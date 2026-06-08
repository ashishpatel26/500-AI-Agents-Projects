import heroImage from "../../images/AIAgentUseCase.jpg";
import industryImage from "../../images/industry_usecase1.png";
import repoReadme from "../../README.md?raw";
import agentsReadme from "../../agents/README.md?raw";
import courseReadme from "../../crewai_mcp_course/README.md?raw";

const agentFiles = import.meta.glob(
  "../../agents/*/{README.md,agent.py,metadata.yaml,requirements.txt}",
  {
    eager: true,
    import: "default",
    query: "?raw",
  },
);

const courseFiles = import.meta.glob("../../crewai_mcp_course/**/*.{md,py,txt}", {
  eager: true,
  import: "default",
  query: "?raw",
});

export function stripMarkdown(value = "") {
  return String(value)
    .replace(/<[^>]*>/g, " ")
    .replace(/!\[[^\]]*]\([^)]+\)/g, " ")
    .replace(/\[([^\]]+)]\([^)]+\)/g, "$1")
    .replace(/[*_`>#]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

export function slugify(value = "item") {
  const cleaned = stripMarkdown(value)
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");

  return cleaned || "item";
}

function titleCase(value = "") {
  return stripMarkdown(value)
    .replace(/^[^A-Za-z0-9]+/, "")
    .replace(/[-_]+/g, " ")
    .split(" ")
    .filter(Boolean)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

function formatFramework(value = "") {
  const key = slugify(value);
  const names = {
    agno: "Agno",
    autogen: "AutoGen",
    crewai: "CrewAI",
    langchain: "LangChain",
    langgraph: "LangGraph",
    llamaindex: "LlamaIndex",
    "llama-index": "LlamaIndex",
  };
  return names[key] || titleCase(value || "Python");
}

function cleanCell(value = "") {
  return stripMarkdown(value)
    .replace(/^[^A-Za-z0-9]+/, "")
    .replace(/\s+/g, " ")
    .trim();
}

function extractUrl(value = "") {
  const markdownUrls = Array.from(String(value).matchAll(/\]\((https?:\/\/[^)]+)\)/g))
    .map((match) => match[1])
    .filter((url) => !url.includes("img.shields.io"));
  if (markdownUrls.length > 0) {
    return markdownUrls[markdownUrls.length - 1];
  }

  const directUrls = String(value)
    .match(/https?:\/\/[^\s)]+/g)
    ?.filter((url) => !url.includes("img.shields.io"));
  return directUrls?.[directUrls.length - 1] || "";
}

function splitTableRow(line = "") {
  return line
    .trim()
    .replace(/^\|/, "")
    .replace(/\|$/, "")
    .split("|")
    .map((cell) => cell.trim());
}

function isDividerRow(line = "") {
  return /^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(line);
}

function getHeaderKey(header = "") {
  return stripMarkdown(header).toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
}

function inferFramework(source = "") {
  if (/crewai/i.test(source)) return "CrewAI";
  if (/autogen/i.test(source)) return "AutoGen";
  if (/agno/i.test(source)) return "Agno";
  if (/langgraph/i.test(source)) return "LangGraph";
  if (/llamaindex|llama index/i.test(source)) return "LlamaIndex";
  return "Cross-industry";
}

function isUseCaseTable(headers, sourceHeading) {
  const headerText = headers.map(getHeaderKey).join(" ");
  if (/navigation guide|framework comparison/i.test(sourceHeading)) return false;
  return (
    /description/.test(headerText) &&
    /use case|project|agent|example/.test(headerText) &&
    /code|github|notebook|link|project/.test(headerText)
  );
}

function pickRowValue(row, candidates) {
  const key = Object.keys(row).find((item) =>
    candidates.some((candidate) => item.includes(candidate)),
  );
  return key ? row[key] : "";
}

export function parseReadmeUseCases(markdown = repoReadme) {
  const lines = markdown.split(/\r?\n/);
  const records = [];
  const usedIds = new Set();
  let inFence = false;
  let h2 = "";
  let h3 = "";
  let subheading = "";

  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    if (/^\s*```/.test(line)) {
      inFence = !inFence;
      continue;
    }
    if (inFence) continue;

    const heading = line.match(/^(#{2,4})\s+(.+)$/);
    if (heading) {
      const level = heading[1].length;
      const value = cleanCell(heading[2]);
      if (level === 2) {
        h2 = value;
        h3 = "";
        subheading = "";
      } else if (level === 3) {
        h3 = value;
        subheading = "";
      } else {
        subheading = value;
      }
      continue;
    }

    const boldHeading = line.match(/^\*\*([^*]+)\*\*\s*$/);
    if (boldHeading) {
      subheading = cleanCell(boldHeading[1]);
      continue;
    }

    if (!line.trim().startsWith("|") || !lines[index + 1] || !isDividerRow(lines[index + 1])) {
      continue;
    }

    const headers = splitTableRow(line);
    const sourceHeading = [h2, h3, subheading].filter(Boolean).join(" / ");
    if (!isUseCaseTable(headers, sourceHeading)) {
      continue;
    }

    index += 2;
    while (index < lines.length && lines[index].trim().startsWith("|")) {
      const cells = splitTableRow(lines[index]);
      if (cells.length >= headers.length - 1) {
        const row = {};
        headers.forEach((header, cellIndex) => {
          row[getHeaderKey(header)] = cells[cellIndex] || "";
        });

        const title =
          cleanCell(pickRowValue(row, ["use case", "project", "agent", "example"])) ||
          cleanCell(cells[0]);
        const description = cleanCell(pickRowValue(row, ["description", "best for"]));
        const industry = cleanCell(pickRowValue(row, ["industry", "domain", "category"]));
        const url = extractUrl(cells.join(" "));

        if (title && description) {
          const baseId = slugify(`${sourceHeading}-${title}`);
          let id = baseId;
          let suffix = 2;
          while (usedIds.has(id)) {
            id = `${baseId}-${suffix}`;
            suffix += 1;
          }
          usedIds.add(id);

          records.push({
            id,
            title,
            description,
            industry: industry || "General",
            framework: inferFramework(sourceHeading),
            sourceHeading,
            sourceGroup: h2,
            sourceSubheading: [h3, subheading].filter(Boolean).join(" / "),
            url,
            resourceType: /notebook|ipynb/i.test(url) ? "Notebook" : "Code",
            tags: [
              inferFramework(sourceHeading),
              industry || "General",
              h2,
              h3,
              subheading,
            ].filter(Boolean),
          });
        }
      }
      index += 1;
    }
    index -= 1;
  }

  return records;
}

function parseYaml(raw = "") {
  const data = {};
  raw.split(/\r?\n/).forEach((line) => {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#") || !trimmed.includes(":")) return;
    const [key, ...rest] = trimmed.split(":");
    const value = rest.join(":").trim();
    if (value.startsWith("[") && value.endsWith("]")) {
      data[key.trim()] = value
        .slice(1, -1)
        .split(",")
        .map((item) => item.trim().replace(/^["']|["']$/g, ""))
        .filter(Boolean);
    } else {
      data[key.trim()] = value.replace(/^["']|["']$/g, "");
    }
  });
  return data;
}

function firstHeading(markdown = "") {
  return cleanCell(markdown.match(/^#\s+(.+)$/m)?.[1] || "");
}

function extractSection(markdown = "", headingPattern) {
  const lines = markdown.split(/\r?\n/);
  const start = lines.findIndex((line) => {
    const heading = line.match(/^#{2,4}\s+(.+)$/);
    return heading && headingPattern.test(heading[1]);
  });
  if (start === -1) return "";

  const output = [];
  for (let index = start + 1; index < lines.length; index += 1) {
    if (/^#{2,4}\s+/.test(lines[index])) break;
    output.push(lines[index]);
  }
  return output.join("\n").trim();
}

function extractList(section = "", limit = 6) {
  return section
    .split(/\r?\n/)
    .map((line) => line.match(/^\s*(?:[-*]|\d+\.)\s+(.+)$/)?.[1])
    .filter(Boolean)
    .map(cleanCell)
    .filter(Boolean)
    .slice(0, limit);
}

function extractCodeFences(section = "") {
  return Array.from(section.matchAll(/```(?:bash|sh|shell)?\s*\n([\s\S]*?)```/g))
    .map((match) => match[1].trim())
    .filter(Boolean);
}

function extractPythonConcepts(code = "") {
  const functions = Array.from(code.matchAll(/^def\s+([A-Za-z_][A-Za-z0-9_]*)/gm)).map(
    (match) => match[1],
  );
  const classes = Array.from(code.matchAll(/^class\s+([A-Za-z_][A-Za-z0-9_]*)/gm)).map(
    (match) => match[1],
  );
  const signals = [
    code.includes("StateGraph") && "state graph",
    code.includes("Crew(") && "crew orchestration",
    code.includes("Agent(") && "agent roles",
    code.includes("Task(") && "task pipeline",
    code.includes("Tool") && "tool calls",
    code.includes("argparse") && "command line interface",
    code.includes("sqlite3") && "local database",
    code.includes("pandas") && "dataframe processing",
    code.includes("Tavily") && "web search",
  ].filter(Boolean);

  return {
    functions: functions.slice(0, 10),
    classes: classes.slice(0, 8),
    signals,
  };
}

function buildAgents() {
  const folders = {};
  Object.entries(agentFiles).forEach(([path, raw]) => {
    const match = path.match(/agents\/([^/]+)\/([^/]+)$/);
    if (!match) return;
    const [, folder, fileName] = match;
    folders[folder] = folders[folder] || {};
    folders[folder][fileName] = raw;
  });

  return Object.entries(folders)
    .map(([folder, files]) => {
      const metadata = parseYaml(files["metadata.yaml"] || "");
      const readme = files["README.md"] || "";
      const code = files["agent.py"] || "";
      const setupSection = extractSection(readme, /setup|installation/i);
      const runSection = extractSection(readme, /run|usage/i);
      const features =
        extractList(extractSection(readme, /what it does/i), 7).length > 0
          ? extractList(extractSection(readme, /what it does/i), 7)
          : extractList(extractSection(readme, /features|use cases/i), 7);
      const title = titleCase(firstHeading(readme) || metadata.title || folder);
      const number = folder.match(/^\d+/)?.[0] || "";
      const concepts = extractPythonConcepts(code);

      return {
        id: folder,
        slug: folder,
        number,
        title,
        description: metadata.description || cleanCell(readme.split(/\r?\n/)[2] || ""),
        framework: formatFramework(metadata.framework || "Python"),
        llm: metadata.llm || "Configurable",
        industry: titleCase(metadata.industry || "General"),
        difficulty: titleCase(metadata.difficulty || "Intermediate"),
        tags: Array.isArray(metadata.tags) ? metadata.tags : [],
        language: titleCase(metadata.language || "Python"),
        localPath: `agents/${folder}`,
        entrypoint: metadata.entrypoint || "agent.py",
        requirements: metadata.requirements || "requirements.txt",
        readme,
        code,
        requirementsText: files["requirements.txt"] || "",
        metadataText: files["metadata.yaml"] || "",
        features,
        setupCommands: extractCodeFences(setupSection),
        runCommands: extractCodeFences(runSection),
        concepts,
      };
    })
    .sort((a, b) => a.slug.localeCompare(b.slug, undefined, { numeric: true }));
}

function getCourseFile(pathSuffix) {
  const entry = Object.entries(courseFiles).find(([path]) => path.endsWith(pathSuffix));
  return entry ? entry[1] : "";
}

const courseLessons = [
  {
    slug: "lesson-01",
    number: "01",
    title: "First CrewAI Researcher",
    summary:
      "Build a single researcher agent, give it a clear role, run one task, and inspect the response path.",
    files: [
      {
        label: "agent.py",
        path: "crewai_mcp_course/lesson_01/agent.py",
        content: getCourseFile("lesson_01/agent.py"),
      },
      {
        label: "requirements.txt",
        path: "crewai_mcp_course/lesson_01/requirements.txt",
        content: getCourseFile("lesson_01/requirements.txt"),
      },
    ],
    objectives: [
      "Install the CrewAI lesson dependencies",
      "Define a role-driven research agent",
      "Attach the agent to one clear task",
      "Run the crew and read the final output",
    ],
    runCommands: ["cd crewai_mcp_course/lesson_01", "pip install -r requirements.txt", "python agent.py"],
  },
  {
    slug: "lesson-02",
    number: "02",
    title: "Multi-Agent Research Crew",
    summary:
      "Split research, writing, and editing responsibilities into a sequential CrewAI workflow.",
    files: [
      {
        label: "agent.py",
        path: "crewai_mcp_course/lesson_02/agent.py",
        content: getCourseFile("lesson_02/agent.py"),
      },
      {
        label: "requirements.txt",
        path: "crewai_mcp_course/lesson_02/requirements.txt",
        content: getCourseFile("lesson_02/requirements.txt"),
      },
    ],
    objectives: [
      "Create multiple specialist agents",
      "Connect tasks into a sequential process",
      "Pass context from researcher to writer to editor",
      "Understand where tools fit into CrewAI",
    ],
    runCommands: ["cd crewai_mcp_course/lesson_02", "pip install -r requirements.txt", "python agent.py"],
  },
  {
    slug: "lesson-03",
    number: "03",
    title: "CrewAI With FastMCP-Style Tools",
    summary:
      "Use a FastMCP-style tool surface to let CrewAI agents query structured project data and produce a status report.",
    files: [
      {
        label: "agent.py",
        path: "crewai_mcp_course/lesson_03/agent.py",
        content: getCourseFile("lesson_03/agent.py"),
      },
      {
        label: "mcp_server.py",
        path: "crewai_mcp_course/lesson_03/mcp_server.py",
        content: getCourseFile("lesson_03/mcp_server.py"),
      },
      {
        label: "requirements.txt",
        path: "crewai_mcp_course/lesson_03/requirements.txt",
        content: getCourseFile("lesson_03/requirements.txt"),
      },
    ],
    objectives: [
      "Model a tool contract that resembles MCP server access",
      "Let agents request project records through tools",
      "Generate a management-ready project status report",
      "See how MCP-style boundaries improve agent design",
    ],
    runCommands: ["cd crewai_mcp_course/lesson_03", "pip install -r requirements.txt", "python agent.py"],
  },
];

export const frameworks = [
  {
    slug: "langgraph",
    name: "LangGraph",
    accent: "cyan",
    bestFor: "Stateful workflows, graph control, retries, RAG, and production routing.",
    decision: "Choose it when the agent needs explicit state transitions and reliable recovery paths.",
  },
  {
    slug: "crewai",
    name: "CrewAI",
    accent: "green",
    bestFor: "Role-based teams, business automation, repeatable task handoffs, and fast prototypes.",
    decision: "Choose it when the project maps naturally to specialists with goals and tasks.",
  },
  {
    slug: "autogen",
    name: "AutoGen",
    accent: "amber",
    bestFor: "Code generation, research collaboration, feedback loops, and executable experiments.",
    decision: "Choose it when agents need to talk, critique, run code, and iterate.",
  },
  {
    slug: "agno",
    name: "Agno",
    accent: "rose",
    bestFor: "Lightweight tool agents, quick iteration, model flexibility, and compact apps.",
    decision: "Choose it when you want a focused tool-calling agent with low ceremony.",
  },
  {
    slug: "llamaindex",
    name: "LlamaIndex",
    accent: "violet",
    bestFor: "Document Q&A, enterprise retrieval, data connectors, and knowledge workflows.",
    decision: "Choose it when the data pipeline matters as much as the agent behavior.",
  },
];

export const catalog = {
  repoReadme,
  agentsReadme,
  courseReadme,
  agents: buildAgents(),
  useCases: parseReadmeUseCases(repoReadme),
  courseLessons,
  frameworks,
  images: {
    hero: heroImage,
    industry: industryImage,
  },
};
