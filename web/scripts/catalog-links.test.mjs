import assert from "node:assert/strict";
import { after, before, test } from "node:test";
import { fileURLToPath } from "node:url";
import { createServer as createHttpServer } from "node:http";
import { createServer } from "vite";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";

let server;
let parseReadmeUseCases;
let catalog;

before(async () => {
  server = await createServer({
    root: fileURLToPath(new URL("..", import.meta.url)),
    server: { middlewareMode: true, watch: null, hmr: { server: createHttpServer() } },
  });
  ({ parseReadmeUseCases, catalog } = await server.ssrLoadModule("/src/content.js"));
});

after(async () => { await server?.close(); });

function parseLinks(links) {
  return parseReadmeUseCases(`## Software Development
| Use Case | Industry | Description | Project Link |
| --- | --- | --- | --- |
| Example | Software | Tests an application | ${links} |`)[0];
}

test("keeps repository and website destinations while excluding badge images", () => {
  const entry = parseLinks("[![GitHub](https://img.shields.io/badge/code)](https://github.com/example/project) · [Website](https://example.com)");
  assert.deepEqual(entry.urls, ["https://github.com/example/project", "https://example.com"]);
  assert.equal(entry.url, "https://example.com");
});

test("preserves the primary destination for single-link and plain-URL rows", () => {
  for (const link of ["[Code](https://github.com/example/project)", "https://github.com/example/project"]) {
    const entry = parseLinks(link);
    assert.deepEqual(entry.urls, ["https://github.com/example/project"]);
    assert.equal(entry.url, "https://github.com/example/project");
  }
});

test("does not render duplicate destinations", () => {
  const entry = parseLinks("[Code](https://example.com) · [Website](https://example.com)");
  assert.deepEqual(entry.urls, ["https://example.com"]);
});

test("deduplication does not change an existing redirect destination", () => {
  const entry = parseLinks("[Code](https://github.com/example/project) · [Website](https://example.com) · [Source](https://github.com/example/project)");
  assert.deepEqual(entry.urls, ["https://github.com/example/project", "https://example.com"]);
  assert.equal(entry.url, "https://github.com/example/project");
});

test("the agent-qa catalog entry retains both official destinations", () => {
  const entry = catalog.useCases.find((item) => item.title === "agent-qa");
  assert.deepEqual(entry.urls, ["https://github.com/vostride/agent-qa", "https://vostride.com"]);
});

test("the use-case detail page exposes both destinations as links", async () => {
  const entry = catalog.useCases.find((item) => item.title === "agent-qa");
  const { default: App } = await server.ssrLoadModule("/src/App.jsx");
  const previousWindow = globalThis.window;
  globalThis.window = { location: { hash: `#/use-cases/${entry.id}` } };
  try {
    const html = renderToStaticMarkup(createElement(App));
    assert.match(html, /href="https:\/\/github\.com\/vostride\/agent-qa"/);
    assert.match(html, /href="https:\/\/vostride\.com"/);
    assert.match(html, /Open GitHub/);
    assert.match(html, /Open website/);
  } finally {
    if (previousWindow === undefined) delete globalThis.window;
    else globalThis.window = previousWindow;
  }
});
