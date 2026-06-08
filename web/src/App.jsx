import { useEffect, useMemo, useState } from "react";
import {
  ArrowRight,
  BookOpen,
  Boxes,
  CheckCircle2,
  Code2,
  Copy,
  ExternalLink,
  FileText,
  Filter,
  GitBranch,
  Github,
  GraduationCap,
  Layers3,
  Network,
  Play,
  Search,
  Terminal,
  Workflow,
  Zap,
} from "lucide-react";
import { catalog, slugify, stripMarkdown } from "./content.js";

const routeLabels = [
  { path: "/", label: "Atlas" },
  { path: "/course", label: "Course" },
  { path: "/agents", label: "Agents" },
  { path: "/use-cases", label: "Use cases" },
  { path: "/frameworks", label: "Frameworks" },
];

function useHashRoute() {
  const [route, setRoute] = useState(() => window.location.hash.slice(1) || "/");

  useEffect(() => {
    const onHashChange = () => setRoute(window.location.hash.slice(1) || "/");
    window.addEventListener("hashchange", onHashChange);
    return () => window.removeEventListener("hashchange", onHashChange);
  }, []);

  return route;
}

function pathFor(route) {
  return `#${route}`;
}

function normalize(value = "") {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
}

function matchesQuery(item, query) {
  if (!query) return true;
  const haystack = normalize(
    [
      item.title,
      item.description,
      item.framework,
      item.industry,
      item.sourceHeading,
      item.tags?.join(" "),
    ].join(" "),
  );
  return normalize(query)
    .split(" ")
    .filter(Boolean)
    .every((part) => haystack.includes(part));
}

function getIntro(markdown = "", fallback = "") {
  const lines = markdown
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean)
    .filter((line) => !line.startsWith("#") && !line.startsWith("```"));

  return stripMarkdown(lines.find((line) => line.length > 30) || fallback).slice(0, 260);
}

function Shell({ route, children }) {
  return (
    <div className="app-shell">
      <header className="topbar">
        <a className="brand" href={pathFor("/")}>
          <span className="brand-mark">
            <Network size={18} aria-hidden="true" />
          </span>
          <span>
            <strong>AI Agents Atlas</strong>
            <small>500+ project map</small>
          </span>
        </a>

        <nav className="nav-links" aria-label="Main navigation">
          {routeLabels.map((item) => (
            <a
              className={
                route === item.path || (item.path !== "/" && route.startsWith(`${item.path}/`))
                  ? "active"
                  : ""
              }
              href={pathFor(item.path)}
              key={item.path}
            >
              {item.label}
            </a>
          ))}
        </nav>

        <a className="icon-link" href="https://github.com/ashishpatel26/500-AI-Agents-Projects">
          <Github size={18} aria-hidden="true" />
          <span>GitHub</span>
        </a>
      </header>
      <main>{children}</main>
    </div>
  );
}

function StatStrip() {
  const stats = [
    { label: "Runnable agents", value: catalog.agents.length, icon: Code2 },
    { label: "README use cases", value: catalog.useCases.length, icon: Boxes },
    { label: "Framework families", value: catalog.frameworks.length, icon: Workflow },
    { label: "Course lessons", value: catalog.courseLessons.length, icon: GraduationCap },
  ];

  return (
    <section className="stat-strip" aria-label="Repository statistics">
      {stats.map((stat) => {
        const Icon = stat.icon;
        return (
          <article className="stat-tile" key={stat.label}>
            <Icon size={18} aria-hidden="true" />
            <strong>{stat.value}</strong>
            <span>{stat.label}</span>
          </article>
        );
      })}
    </section>
  );
}

function GraphHero() {
  const nodes = [
    { label: "CrewAI course", path: "/course", x: 11, y: 22, tone: "green" },
    { label: "Runnable agents", path: "/agents", x: 52, y: 13, tone: "cyan" },
    { label: "Use cases", path: "/use-cases", x: 74, y: 48, tone: "amber" },
    { label: "Frameworks", path: "/frameworks", x: 24, y: 65, tone: "rose" },
    { label: "Code pages", path: "/agents/01-web-research-agent", x: 54, y: 78, tone: "violet" },
  ];

  return (
    <section className="hero-grid">
      <div className="hero-copy">
        <p className="eyebrow">Course front page plus project atlas</p>
        <h1>500+ AI Agent Projects</h1>
        <p>
          A premium React atlas for learning, browsing, running, and redirecting into the
          strongest AI agent examples in this repository.
        </p>
        <div className="hero-actions">
          <a className="primary-action" href={pathFor("/course")}>
            <GraduationCap size={18} aria-hidden="true" />
            Start course
          </a>
          <a className="secondary-action" href={pathFor("/use-cases")}>
            <Search size={18} aria-hidden="true" />
            Browse use cases
          </a>
        </div>
      </div>

      <div className="graph-stage" aria-label="Interactive agent atlas graph">
        <svg className="edge-layer" viewBox="0 0 100 100" preserveAspectRatio="none">
          <path className="graph-edge edge-one" d="M12 25 C30 8, 42 12, 52 16" />
          <path className="graph-edge edge-two" d="M54 18 C69 23, 78 33, 75 50" />
          <path className="graph-edge edge-three" d="M72 51 C61 71, 51 78, 27 67" />
          <path className="graph-edge edge-four" d="M25 65 C12 54, 8 38, 12 25" />
          <path className="graph-edge edge-five" d="M53 17 C48 39, 48 60, 54 78" />
        </svg>
        {nodes.map((node) => (
          <a
            className={`graph-node tone-${node.tone}`}
            href={pathFor(node.path)}
            key={node.label}
            style={{ left: `${node.x}%`, top: `${node.y}%` }}
          >
            <span />
            {node.label}
          </a>
        ))}
        <div className="graph-console">
          <span>agent_state</span>
          <strong>ready</strong>
          <small>nodes: {catalog.agents.length + catalog.frameworks.length}</small>
        </div>
      </div>
    </section>
  );
}

function SearchPanel({ compact = false }) {
  const [query, setQuery] = useState("");
  const agentMatches = catalog.agents.filter((agent) => matchesQuery(agent, query)).slice(0, 4);
  const useCaseMatches = catalog.useCases.filter((useCase) => matchesQuery(useCase, query)).slice(0, 6);

  return (
    <section className={compact ? "search-panel compact" : "search-panel"}>
      <label className="search-box">
        <Search size={18} aria-hidden="true" />
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Search agents, use cases, frameworks, industries"
        />
      </label>

      <div className="search-results">
        {[...agentMatches, ...useCaseMatches].map((item) => {
          const isAgent = Boolean(item.localPath);
          return (
            <a
              className="result-row"
              href={pathFor(isAgent ? `/agents/${item.slug}` : `/use-cases/${item.id}`)}
              key={`${isAgent ? "agent" : "case"}-${item.id}`}
            >
              <span className={`mini-dot ${slugify(item.framework)}`} />
              <strong>{item.title}</strong>
              <small>{isAgent ? item.localPath : item.sourceHeading}</small>
            </a>
          );
        })}
      </div>
    </section>
  );
}

function HomePage() {
  const featuredAgents = catalog.agents.slice(0, 6);
  const featuredUseCases = catalog.useCases.slice(0, 8);

  return (
    <>
      <GraphHero />
      <StatStrip />

      <section className="split-section">
        <div className="section-copy">
          <p className="eyebrow">Start here</p>
          <h2>CrewAI with FastMCP-style lessons at the front</h2>
          <p>
            The course is the guided entry point, then the atlas opens into local code agents
            and README-linked external examples.
          </p>
          <a className="inline-action" href={pathFor("/course")}>
            Open course page <ArrowRight size={16} aria-hidden="true" />
          </a>
        </div>
        <CourseRail />
      </section>

      <section className="media-band">
        <img src={catalog.images.hero} alt="AI agent use case map" />
        <div>
          <p className="eyebrow">Live catalog</p>
          <h2>Search every local agent and README table row</h2>
          <SearchPanel compact />
        </div>
      </section>

      <section className="content-band">
        <SectionHeader
          eyebrow="Runnable code"
          title="Local agent implementations"
          action={{ label: "View all agents", href: "/agents" }}
        />
        <div className="card-grid">
          {featuredAgents.map((agent) => (
            <AgentCard agent={agent} key={agent.id} />
          ))}
        </div>
      </section>

      <section className="content-band">
        <SectionHeader
          eyebrow="README use cases"
          title="External projects with dedicated pages"
          action={{ label: "View all use cases", href: "/use-cases" }}
        />
        <div className="usecase-grid">
          {featuredUseCases.map((useCase) => (
            <UseCaseCard useCase={useCase} key={useCase.id} />
          ))}
        </div>
      </section>

      <FrameworkStrip />
    </>
  );
}

function SectionHeader({ eyebrow, title, action }) {
  return (
    <div className="section-header">
      <div>
        <p className="eyebrow">{eyebrow}</p>
        <h2>{title}</h2>
      </div>
      {action ? (
        <a className="inline-action" href={pathFor(action.href)}>
          {action.label} <ArrowRight size={16} aria-hidden="true" />
        </a>
      ) : null}
    </div>
  );
}

function CourseRail() {
  return (
    <div className="course-rail">
      {catalog.courseLessons.map((lesson) => (
        <a className="lesson-row" href={pathFor(`/course/${lesson.slug}`)} key={lesson.slug}>
          <span>{lesson.number}</span>
          <div>
            <strong>{lesson.title}</strong>
            <small>{lesson.summary}</small>
          </div>
          <ArrowRight size={16} aria-hidden="true" />
        </a>
      ))}
    </div>
  );
}

function FrameworkStrip() {
  return (
    <section className="content-band">
      <SectionHeader
        eyebrow="Decision support"
        title="Framework map"
        action={{ label: "Compare frameworks", href: "/frameworks" }}
      />
      <div className="framework-grid">
        {catalog.frameworks.map((framework) => (
          <a
            className={`framework-card tone-${framework.accent}`}
            href={pathFor(`/frameworks/${framework.slug}`)}
            key={framework.slug}
          >
            <strong>{framework.name}</strong>
            <p>{framework.bestFor}</p>
            <span>{framework.decision}</span>
          </a>
        ))}
      </div>
    </section>
  );
}

function AgentCard({ agent }) {
  return (
    <a className="agent-card" href={pathFor(`/agents/${agent.slug}`)}>
      <div className="card-topline">
        <span className={`framework-pill ${slugify(agent.framework)}`}>{agent.framework}</span>
        <small>{agent.difficulty}</small>
      </div>
      <h3>{agent.title}</h3>
      <p>{agent.description}</p>
      <div className="tag-list">
        {[agent.industry, agent.llm, ...agent.tags].filter(Boolean).slice(0, 4).map((tag) => (
          <span key={tag}>{tag}</span>
        ))}
      </div>
    </a>
  );
}

function UseCaseCard({ useCase }) {
  return (
    <article className="usecase-card">
      <div className="card-topline">
        <span className={`framework-pill ${slugify(useCase.framework)}`}>{useCase.framework}</span>
        <small>{useCase.resourceType}</small>
      </div>
      <h3>{useCase.title}</h3>
      <p>{useCase.description}</p>
      <div className="card-actions">
        <a href={pathFor(`/use-cases/${useCase.id}`)}>
          <FileText size={15} aria-hidden="true" />
          Detail
        </a>
        {useCase.url ? (
          <a href={pathFor(`/go/${useCase.id}`)}>
            <ExternalLink size={15} aria-hidden="true" />
            Redirect
          </a>
        ) : null}
      </div>
    </article>
  );
}

function CoursePage() {
  return (
    <>
      <PageHero
        eyebrow="Course"
        title="CrewAI with FastMCP-style integration"
        description={getIntro(catalog.courseReadme, "A practical course for building CrewAI workflows with MCP-style tool boundaries.")}
        icon={GraduationCap}
      />
      <section className="split-section">
        <div className="section-copy">
          <h2>Learning path</h2>
          <p>
            Each lesson has its own page with objectives, run commands, code files, and a code
            walkthrough surface.
          </p>
          <div className="command-stack">
            <CodeBlock
              code={[
                "cd crewai_mcp_course/lesson_01",
                "pip install -r requirements.txt",
                "python agent.py",
              ].join("\n")}
              compact
            />
          </div>
        </div>
        <CourseRail />
      </section>
      <section className="content-band">
        <SectionHeader eyebrow="Lessons" title="Separate lesson pages" />
        <div className="lesson-grid">
          {catalog.courseLessons.map((lesson) => (
            <a className="lesson-card" href={pathFor(`/course/${lesson.slug}`)} key={lesson.slug}>
              <span>{lesson.number}</span>
              <h3>{lesson.title}</h3>
              <p>{lesson.summary}</p>
              <ul>
                {lesson.objectives.slice(0, 3).map((objective) => (
                  <li key={objective}>
                    <CheckCircle2 size={15} aria-hidden="true" />
                    {objective}
                  </li>
                ))}
              </ul>
            </a>
          ))}
        </div>
      </section>
    </>
  );
}

function LessonPage({ lesson }) {
  const [selectedFile, setSelectedFile] = useState(lesson.files[0]?.label || "");
  const file = lesson.files.find((item) => item.label === selectedFile) || lesson.files[0];

  return (
    <>
      <PageHero
        eyebrow={`Lesson ${lesson.number}`}
        title={lesson.title}
        description={lesson.summary}
        icon={BookOpen}
      />
      <section className="detail-layout">
        <aside className="detail-aside">
          <h2>Objectives</h2>
          <ul className="check-list">
            {lesson.objectives.map((objective) => (
              <li key={objective}>
                <CheckCircle2 size={16} aria-hidden="true" />
                {objective}
              </li>
            ))}
          </ul>
          <h2>Run</h2>
          <CodeBlock code={lesson.runCommands.join("\n")} compact />
        </aside>
        <article className="detail-main">
          <FileTabs files={lesson.files} selected={selectedFile} onSelect={setSelectedFile} />
          <CodeBlock code={file?.content || "# File content not found"} />
          <CodeExplanation code={file?.content || ""} context="lesson" />
        </article>
      </section>
    </>
  );
}

function AgentsPage() {
  const [query, setQuery] = useState("");
  const [framework, setFramework] = useState("all");
  const frameworks = ["all", ...new Set(catalog.agents.map((agent) => slugify(agent.framework)))];
  const agents = catalog.agents.filter(
    (agent) =>
      matchesQuery(agent, query) &&
      (framework === "all" || slugify(agent.framework) === framework),
  );

  return (
    <>
      <PageHero
        eyebrow="Runnable agents"
        title="Local code pages for every implementation"
        description="Each agent page explains the framework, setup, run commands, architecture, and code structure from the files in agents/."
        icon={Code2}
      />
      <CatalogToolbar query={query} onQuery={setQuery} filters={frameworks} filter={framework} onFilter={setFramework} />
      <section className="content-band">
        <div className="card-grid">
          {agents.map((agent) => (
            <AgentCard agent={agent} key={agent.id} />
          ))}
        </div>
      </section>
    </>
  );
}

function AgentPage({ agent }) {
  const [selectedFile, setSelectedFile] = useState("agent.py");
  const files = [
    { label: "agent.py", path: `${agent.localPath}/agent.py`, content: agent.code },
    { label: "README.md", path: `${agent.localPath}/README.md`, content: agent.readme },
    { label: "requirements.txt", path: `${agent.localPath}/requirements.txt`, content: agent.requirementsText },
    { label: "metadata.yaml", path: `${agent.localPath}/metadata.yaml`, content: agent.metadataText },
  ];
  const selected = files.find((file) => file.label === selectedFile) || files[0];
  const related = catalog.agents
    .filter((item) => item.slug !== agent.slug && item.framework === agent.framework)
    .slice(0, 3);

  return (
    <>
      <PageHero
        eyebrow={`${agent.framework} agent`}
        title={agent.title}
        description={agent.description}
        icon={GitBranch}
      />
      <section className="detail-layout">
        <aside className="detail-aside">
          <MetadataPanel agent={agent} />
          <h2>Run in 5 minutes</h2>
          <CodeBlock
            code={
              (agent.runCommands[0] || agent.setupCommands[0]) ??
              [`cd ${agent.localPath}`, "pip install -r requirements.txt", "python agent.py"].join("\n")
            }
            compact
          />
          <h2>Architecture</h2>
          <FlowTrace agent={agent} />
        </aside>
        <article className="detail-main">
          <section className="explain-panel">
            <h2>How it works</h2>
            <p>{getIntro(agent.readme, agent.description)}</p>
            <ul className="check-list">
              {(agent.features.length ? agent.features : defaultAgentSteps(agent)).map((feature) => (
                <li key={feature}>
                  <CheckCircle2 size={16} aria-hidden="true" />
                  {feature}
                </li>
              ))}
            </ul>
          </section>
          <FileTabs files={files} selected={selectedFile} onSelect={setSelectedFile} />
          <CodeBlock code={selected.content || "# File content not found"} />
          <CodeExplanation code={selected.content || ""} context={selected.label} agent={agent} />
          {related.length ? (
            <section className="related-band">
              <h2>Related {agent.framework} agents</h2>
              <div className="mini-card-grid">
                {related.map((item) => (
                  <AgentCard agent={item} key={item.id} />
                ))}
              </div>
            </section>
          ) : null}
        </article>
      </section>
    </>
  );
}

function defaultAgentSteps(agent) {
  return [
    `Loads configuration for ${agent.llm}`,
    `Creates a ${agent.framework} workflow around the core task`,
    "Accepts user input through the command line or defaults",
    "Calls tools, models, or local data helpers",
    "Returns a structured result for the user",
  ];
}

function MetadataPanel({ agent }) {
  const rows = [
    ["Path", agent.localPath],
    ["Framework", agent.framework],
    ["Difficulty", agent.difficulty],
    ["Industry", agent.industry],
    ["Model", agent.llm],
    ["Language", agent.language],
  ];

  return (
    <section className="metadata-panel">
      <h2>Project metadata</h2>
      {rows.map(([label, value]) => (
        <div className="meta-row" key={label}>
          <span>{label}</span>
          <strong>{value}</strong>
        </div>
      ))}
    </section>
  );
}

function FlowTrace({ agent }) {
  const steps =
    agent.framework === "Langgraph" || agent.framework === "LangGraph"
      ? ["Input", "State", "Node", "Tool", "Response"]
      : agent.framework === "Crewai" || agent.framework === "CrewAI"
        ? ["Goal", "Agent", "Task", "Crew", "Output"]
        : ["Input", "Planner", "Tool", "Model", "Output"];

  return (
    <div className="flow-trace">
      {steps.map((step, index) => (
        <div className="flow-step" key={step}>
          <span>{index + 1}</span>
          <strong>{step}</strong>
        </div>
      ))}
    </div>
  );
}

function UseCasesPage() {
  const [query, setQuery] = useState("");
  const [framework, setFramework] = useState("all");
  const frameworks = ["all", ...new Set(catalog.useCases.map((item) => slugify(item.framework)))];
  const useCases = catalog.useCases.filter(
    (item) =>
      matchesQuery(item, query) &&
      (framework === "all" || slugify(item.framework) === framework),
  );

  return (
    <>
      <PageHero
        eyebrow="README catalog"
        title="Dedicated page for every README use case"
        description="The catalog is parsed from the repository README tables, so each external project gets a page, source section, and redirect route."
        icon={Boxes}
      />
      <CatalogToolbar query={query} onQuery={setQuery} filters={frameworks} filter={framework} onFilter={setFramework} />
      <section className="content-band">
        <div className="catalog-count">{useCases.length} matching use cases</div>
        <div className="usecase-grid">
          {useCases.map((useCase) => (
            <UseCaseCard useCase={useCase} key={useCase.id} />
          ))}
        </div>
      </section>
    </>
  );
}

function UseCasePage({ useCase }) {
  const relatedAgents = catalog.agents
    .filter(
      (agent) =>
        slugify(agent.framework) === slugify(useCase.framework) ||
        slugify(agent.industry) === slugify(useCase.industry),
    )
    .slice(0, 4);
  const relatedCases = catalog.useCases
    .filter((item) => item.id !== useCase.id && item.framework === useCase.framework)
    .slice(0, 4);

  return (
    <>
      <PageHero
        eyebrow={useCase.sourceHeading}
        title={useCase.title}
        description={useCase.description}
        icon={ExternalLink}
      />
      <section className="detail-layout">
        <aside className="detail-aside">
          <section className="metadata-panel">
            <h2>Use case metadata</h2>
            <div className="meta-row">
              <span>Framework</span>
              <strong>{useCase.framework}</strong>
            </div>
            <div className="meta-row">
              <span>Industry</span>
              <strong>{useCase.industry}</strong>
            </div>
            <div className="meta-row">
              <span>Source</span>
              <strong>{useCase.sourceHeading}</strong>
            </div>
            <div className="meta-row">
              <span>Resource</span>
              <strong>{useCase.resourceType}</strong>
            </div>
          </section>
          {useCase.url ? (
            <a className="primary-action full-width" href={pathFor(`/go/${useCase.id}`)}>
              <ExternalLink size={18} aria-hidden="true" />
              Open redirect
            </a>
          ) : null}
        </aside>
        <article className="detail-main">
          <section className="explain-panel">
            <h2>What this adds</h2>
            <p>
              This page turns a README table row into a durable catalog entry with context,
              framework grouping, industry filtering, and a redirect route for the source project.
            </p>
            <div className="source-block">
              <strong>{useCase.title}</strong>
              <span>{useCase.description}</span>
              {useCase.url ? <code>{useCase.url}</code> : null}
            </div>
          </section>
          {relatedAgents.length ? (
            <section className="related-band">
              <h2>Related local agents</h2>
              <div className="mini-card-grid">
                {relatedAgents.map((agent) => (
                  <AgentCard agent={agent} key={agent.id} />
                ))}
              </div>
            </section>
          ) : null}
          {relatedCases.length ? (
            <section className="related-band">
              <h2>Similar use cases</h2>
              <div className="usecase-grid compact-grid">
                {relatedCases.map((item) => (
                  <UseCaseCard useCase={item} key={item.id} />
                ))}
              </div>
            </section>
          ) : null}
        </article>
      </section>
    </>
  );
}

function RedirectPage({ useCase }) {
  useEffect(() => {
    if (!useCase?.url) return undefined;
    const timer = window.setTimeout(() => {
      window.location.href = useCase.url;
    }, 900);
    return () => window.clearTimeout(timer);
  }, [useCase]);

  if (!useCase) return <NotFound />;

  return (
    <PageHero
      eyebrow="Redirect"
      title={useCase.title}
      description={`Opening ${useCase.url || "the source project"}.`}
      icon={ExternalLink}
      action={
        useCase.url
          ? {
              label: "Open now",
              href: useCase.url,
              external: true,
            }
          : null
      }
    />
  );
}

function FrameworksPage({ frameworkSlug }) {
  const selected = catalog.frameworks.find((item) => item.slug === frameworkSlug);
  const visibleFrameworks = selected ? [selected] : catalog.frameworks;

  return (
    <>
      <PageHero
        eyebrow="Frameworks"
        title={selected ? selected.name : "Choose the right agent framework"}
        description={
          selected
            ? selected.decision
            : "Compare the main framework families represented in this repository, then jump into matching agents and examples."
        }
        icon={Workflow}
      />
      <section className="content-band">
        <div className="framework-grid">
          {visibleFrameworks.map((framework) => {
            const agents = catalog.agents.filter(
              (agent) => slugify(agent.framework) === framework.slug,
            );
            const useCases = catalog.useCases.filter(
              (useCase) => slugify(useCase.framework) === framework.slug,
            );
            return (
              <article className={`framework-detail tone-${framework.accent}`} key={framework.slug}>
                <div>
                  <h2>{framework.name}</h2>
                  <p>{framework.bestFor}</p>
                  <span>{framework.decision}</span>
                </div>
                <div className="framework-stats">
                  <strong>{agents.length}</strong>
                  <span>local agents</span>
                  <strong>{useCases.length}</strong>
                  <span>README use cases</span>
                </div>
                <a className="inline-action" href={pathFor(`/frameworks/${framework.slug}`)}>
                  Open framework <ArrowRight size={16} aria-hidden="true" />
                </a>
              </article>
            );
          })}
        </div>
      </section>
      {selected ? (
        <section className="content-band">
          <SectionHeader eyebrow={selected.name} title="Matching examples" />
          <div className="card-grid">
            {catalog.agents
              .filter((agent) => slugify(agent.framework) === selected.slug)
              .slice(0, 6)
              .map((agent) => (
                <AgentCard agent={agent} key={agent.id} />
              ))}
          </div>
        </section>
      ) : null}
    </>
  );
}

function CatalogToolbar({ query, onQuery, filters, filter, onFilter }) {
  return (
    <section className="catalog-toolbar">
      <label className="search-box">
        <Search size={18} aria-hidden="true" />
        <input
          value={query}
          onChange={(event) => onQuery(event.target.value)}
          placeholder="Search catalog"
        />
      </label>
      <div className="filter-row" aria-label="Framework filter">
        <Filter size={17} aria-hidden="true" />
        {filters.map((item) => (
          <button
            className={filter === item ? "active" : ""}
            onClick={() => onFilter(item)}
            type="button"
            key={item}
          >
            {item === "all" ? "All" : catalog.frameworks.find((fw) => fw.slug === item)?.name || item}
          </button>
        ))}
      </div>
    </section>
  );
}

function PageHero({ eyebrow, title, description, icon: Icon, action }) {
  return (
    <section className="page-hero">
      <div>
        <p className="eyebrow">{eyebrow}</p>
        <h1>{title}</h1>
        <p>{description}</p>
        {action ? (
          <a
            className="primary-action"
            href={action.external ? action.href : pathFor(action.href)}
            rel={action.external ? "noreferrer" : undefined}
          >
            <ExternalLink size={18} aria-hidden="true" />
            {action.label}
          </a>
        ) : null}
      </div>
      <div className="page-hero-icon" aria-hidden="true">
        <Icon size={42} />
      </div>
    </section>
  );
}

function FileTabs({ files, selected, onSelect }) {
  return (
    <div className="file-tabs" role="tablist" aria-label="Files">
      {files.map((file) => (
        <button
          className={selected === file.label ? "active" : ""}
          key={file.label}
          onClick={() => onSelect(file.label)}
          type="button"
        >
          <FileText size={15} aria-hidden="true" />
          {file.label}
        </button>
      ))}
    </div>
  );
}

function CodeBlock({ code, compact = false }) {
  const [copied, setCopied] = useState(false);
  const copy = async () => {
    await navigator.clipboard?.writeText(code);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1200);
  };

  return (
    <div className={compact ? "code-block compact" : "code-block"}>
      <div className="code-toolbar">
        <span>
          <Terminal size={15} aria-hidden="true" />
          code
        </span>
        <button onClick={copy} type="button">
          <Copy size={14} aria-hidden="true" />
          {copied ? "Copied" : "Copy"}
        </button>
      </div>
      <pre>
        <code>{code}</code>
      </pre>
    </div>
  );
}

function CodeExplanation({ code, context, agent }) {
  const lines = code.split(/\r?\n/).filter(Boolean);
  const imports = lines.filter((line) => /^import\s|^from\s/.test(line)).slice(0, 6);
  const functions = Array.from(code.matchAll(/^def\s+([A-Za-z_][A-Za-z0-9_]*)/gm)).map(
    (match) => match[1],
  );
  const classes = Array.from(code.matchAll(/^class\s+([A-Za-z_][A-Za-z0-9_]*)/gm)).map(
    (match) => match[1],
  );

  return (
    <section className="code-explain">
      <h2>Code walkthrough</h2>
      <div className="walkthrough-grid">
        <WalkthroughCard
          icon={Layers3}
          title="Imports"
          items={imports.length ? imports : ["No import block in this file section."]}
        />
        <WalkthroughCard
          icon={Zap}
          title="Functions"
          items={functions.length ? functions.slice(0, 8) : ["No top-level functions detected."]}
        />
        <WalkthroughCard
          icon={Network}
          title="Classes"
          items={classes.length ? classes.slice(0, 6) : ["No classes detected."]}
        />
        <WalkthroughCard
          icon={Play}
          title="Role"
          items={[
            context === "agent.py"
              ? `Entrypoint for ${agent?.framework || "the"} implementation.`
              : `Reference file for ${context}.`,
            `${lines.length} non-empty lines are bundled into this page.`,
          ]}
        />
      </div>
    </section>
  );
}

function WalkthroughCard({ icon: Icon, title, items }) {
  return (
    <article className="walk-card">
      <Icon size={18} aria-hidden="true" />
      <h3>{title}</h3>
      <ul>
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </article>
  );
}

function NotFound() {
  return (
    <PageHero
      eyebrow="Missing page"
      title="This atlas page was not found"
      description="The catalog route does not match a local agent, lesson, use case, or framework."
      icon={Search}
      action={{ label: "Back to atlas", href: "/" }}
    />
  );
}

function App() {
  const route = useHashRoute();
  const segments = useMemo(() => route.split("?")[0].split("/").filter(Boolean), [route]);

  let page;
  if (segments.length === 0) {
    page = <HomePage />;
  } else if (segments[0] === "course" && segments.length === 1) {
    page = <CoursePage />;
  } else if (segments[0] === "course") {
    const lesson = catalog.courseLessons.find((item) => item.slug === segments[1]);
    page = lesson ? <LessonPage lesson={lesson} /> : <NotFound />;
  } else if (segments[0] === "agents" && segments.length === 1) {
    page = <AgentsPage />;
  } else if (segments[0] === "agents") {
    const agent = catalog.agents.find((item) => item.slug === segments[1]);
    page = agent ? <AgentPage agent={agent} /> : <NotFound />;
  } else if (segments[0] === "use-cases" && segments.length === 1) {
    page = <UseCasesPage />;
  } else if (segments[0] === "use-cases") {
    const useCase = catalog.useCases.find((item) => item.id === segments[1]);
    page = useCase ? <UseCasePage useCase={useCase} /> : <NotFound />;
  } else if (segments[0] === "go") {
    const useCase = catalog.useCases.find((item) => item.id === segments[1]);
    page = <RedirectPage useCase={useCase} />;
  } else if (segments[0] === "frameworks") {
    page = <FrameworksPage frameworkSlug={segments[1]} />;
  } else {
    page = <NotFound />;
  }

  return <Shell route={route}>{page}</Shell>;
}

export default App;
