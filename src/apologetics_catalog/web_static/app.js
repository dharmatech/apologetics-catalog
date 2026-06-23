const DEFAULT_ROOT_ID = "claim.jesus_created";

let catalog = null;
let currentRootId = DEFAULT_ROOT_ID;
let expandedPaths = new Set();
let firstRenderedPathByEntity = new Map();

document.addEventListener("DOMContentLoaded", () => {
  const openButton = document.querySelector("#open-root");
  const rootInput = document.querySelector("#root-id");

  openButton.addEventListener("click", () => {
    openRoot(rootInput.value);
  });

  rootInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      openRoot(rootInput.value);
    }
  });

  loadCatalog();
});

async function loadCatalog() {
  setStatus("Loading catalog...");
  try {
    const response = await fetch("catalog.json", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    catalog = await response.json();
    const rootFromUrl = new URLSearchParams(window.location.search).get("root");
    const initialRoot = rootFromUrl || DEFAULT_ROOT_ID;
    document.querySelector("#project-summary").textContent = projectSummary();
    document.querySelector("#root-id").value = initialRoot;
    openRoot(initialRoot, { updateUrl: false });
  } catch (error) {
    setStatus(`Could not load catalog.json: ${error.message}`);
  }
}

function openRoot(rawEntityId, options = {}) {
  if (!catalog) {
    return;
  }

  const entityId = rawEntityId.trim();
  if (!entityId) {
    setStatus("Enter an entity ID.");
    return;
  }

  if (!catalog.entities[entityId]) {
    setStatus(`No entity found for id: ${entityId}`);
    renderEmptyTree();
    return;
  }

  currentRootId = entityId;
  expandedPaths = new Set([entityId]);
  document.querySelector("#root-id").value = entityId;

  if (options.updateUrl !== false) {
    const url = new URL(window.location.href);
    url.searchParams.set("root", entityId);
    window.history.replaceState({}, "", url);
  }

  renderTree();
}

function renderTree() {
  firstRenderedPathByEntity = new Map();
  const tree = document.querySelector("#tree");
  tree.replaceChildren(renderNode(currentRootId, currentRootId, [], null));
  setStatus("");
}

function renderEmptyTree() {
  document.querySelector("#tree").replaceChildren();
}

function renderNode(entityId, path, ancestors, parentRelationship) {
  const entity = catalog.entities[entityId];
  const node = document.createElement("article");
  node.className = "node";

  if (!entity) {
    node.appendChild(renderMissingEntity(entityId));
    return node;
  }

  const firstPath = firstRenderedPathByEntity.get(entityId);
  const isRepeated = Boolean(firstPath && firstPath !== path);
  if (!firstPath) {
    firstRenderedPathByEntity.set(entityId, path);
  }

  const isCycle = ancestors.includes(entityId);
  const isExpanded = expandedPaths.has(path);

  node.appendChild(renderNodeHeader(entity, path, isExpanded, isRepeated));

  if (parentRelationship) {
    node.appendChild(renderRelationshipSummary(parentRelationship));
  }

  node.appendChild(renderEntityBody(entity));

  if (!isExpanded) {
    return node;
  }

  if (isCycle) {
    node.appendChild(renderNotice("Cycle detected. This branch is not expanded again."));
    return node;
  }

  if (isRepeated) {
    node.appendChild(renderNotice(`Already shown above: ${entityId}`));
    return node;
  }

  const groups = relationshipGroups(entityId);
  if (groups.length === 0) {
    node.appendChild(renderNotice("No related entities."));
    return node;
  }

  const groupsContainer = document.createElement("div");
  groupsContainer.className = "relationship-groups";
  for (const group of groups) {
    groupsContainer.appendChild(renderRelationshipGroup(group, path, ancestors.concat(entityId)));
  }
  node.appendChild(groupsContainer);

  return node;
}

function renderNodeHeader(entity, path, isExpanded, isRepeated) {
  const header = document.createElement("header");
  header.className = "node-header";

  const left = document.createElement("div");
  left.className = "node-title-block";

  const titleRow = document.createElement("div");
  titleRow.className = "node-title-row";

  const title = document.createElement("h2");
  title.textContent = entity.label || entity.id;
  titleRow.appendChild(title);

  titleRow.appendChild(badge(entity.kind, "kind"));
  if (entity.perspective && entity.perspective.label) {
    titleRow.appendChild(badge(entity.perspective.label, "perspective"));
  }
  if (isRepeated) {
    titleRow.appendChild(badge("Repeated", "repeated"));
  }

  const id = document.createElement("p");
  id.className = "entity-id";
  id.textContent = entity.id;

  left.append(titleRow, id);

  const actions = document.createElement("div");
  actions.className = "node-actions";

  const toggleButton = document.createElement("button");
  toggleButton.type = "button";
  toggleButton.textContent = isExpanded ? "Collapse" : "Expand";
  toggleButton.addEventListener("click", () => {
    if (expandedPaths.has(path)) {
      expandedPaths.delete(path);
    } else {
      expandedPaths.add(path);
    }
    renderTree();
  });

  const rootButton = document.createElement("button");
  rootButton.type = "button";
  rootButton.textContent = "Root";
  rootButton.addEventListener("click", () => {
    openRoot(entity.id);
  });

  actions.append(toggleButton, rootButton);
  header.append(left, actions);
  return header;
}

function renderEntityBody(entity) {
  const body = document.createElement("div");
  body.className = "node-body";

  if (entity.summary && entity.summary !== entity.label) {
    const summary = document.createElement("p");
    summary.className = "summary";
    summary.textContent = entity.summary;
    body.appendChild(summary);
  }

  const details = entity.details || {};
  const fields = detailFields(entity.kind, details);
  if (fields.length > 0) {
    const list = document.createElement("dl");
    list.className = "details";
    for (const field of fields) {
      const value = details[field.key];
      if (value === undefined || value === null || value === "") {
        continue;
      }
      const term = document.createElement("dt");
      term.textContent = field.label;
      const description = document.createElement("dd");
      description.textContent = formatDetailValue(value);
      list.append(term, description);
    }
    if (list.childElementCount > 0) {
      body.appendChild(list);
    }
  }

  return body;
}

function detailFields(kind, details) {
  if (kind === "evidence") {
    return [
      { key: "quotation", label: "Quotation" },
      { key: "paraphrase", label: "Paraphrase" },
      { key: "source_label", label: "Source" },
      { key: "locator", label: "Locator" },
    ];
  }
  if (kind === "interpretation") {
    return [
      { key: "method", label: "Method" },
      { key: "evidence_label", label: "Evidence" },
      { key: "evidence_id", label: "Evidence ID" },
    ];
  }
  if (kind === "argument") {
    return [{ key: "role", label: "Role" }];
  }
  if (kind === "claim") {
    return [
      { key: "proposition", label: "Proposition" },
      { key: "question_id", label: "Question ID" },
    ];
  }
  if (kind === "source") {
    return [
      { key: "type", label: "Type" },
      { key: "edition", label: "Edition" },
      { key: "url", label: "URL" },
      { key: "accessed", label: "Accessed" },
    ];
  }
  return [];
}

function renderRelationshipGroup(group, parentPath, ancestors) {
  const section = document.createElement("section");
  section.className = "relationship-group";

  const heading = document.createElement("h3");
  heading.textContent = group.label;
  section.appendChild(heading);

  const list = document.createElement("div");
  list.className = "children";
  for (const item of group.items) {
    const childPath = `${parentPath}|${item.relationship.id}|${item.entityId}`;
    list.appendChild(renderNode(item.entityId, childPath, ancestors, item.relationship));
  }
  section.appendChild(list);

  return section;
}

function relationshipGroups(entityId) {
  const groups = new Map();
  addRelationshipsToGroups(groups, "incoming", catalog.indexes.incoming[entityId] || []);
  addRelationshipsToGroups(groups, "outgoing", catalog.indexes.outgoing[entityId] || []);
  return Array.from(groups.values()).sort((left, right) => {
    if (left.order !== right.order) {
      return left.order - right.order;
    }
    return left.label.localeCompare(right.label);
  });
}

function addRelationshipsToGroups(groups, direction, relationshipIds) {
  for (const relationshipId of relationshipIds) {
    const relationship = relationshipById(relationshipId);
    if (!relationship) {
      continue;
    }
    const label = relationship.labels[direction] || relationship.type || "Related";
    const order = relationship.group[`${direction}_order`] || 1000;
    const key = `${order}:${label}`;
    if (!groups.has(key)) {
      groups.set(key, { label, order, items: [] });
    }
    groups.get(key).items.push({
      relationship,
      entityId: direction === "incoming" ? relationship.from_id : relationship.to_id,
    });
  }
}

function relationshipById(relationshipId) {
  return catalog.relationships.find((relationship) => relationship.id === relationshipId);
}

function renderRelationshipSummary(relationship) {
  const wrapper = document.createElement("div");
  wrapper.className = "relationship-summary";

  const label = document.createElement("span");
  label.className = "relationship-type";
  label.textContent = relationship.type || "relationship";
  wrapper.appendChild(label);

  if (relationship.summary) {
    const summary = document.createElement("span");
    summary.textContent = relationship.summary;
    wrapper.appendChild(summary);
  }

  return wrapper;
}

function renderMissingEntity(entityId) {
  return renderNotice(`Missing entity: ${entityId}`);
}

function renderNotice(message) {
  const notice = document.createElement("p");
  notice.className = "notice";
  notice.textContent = message;
  return notice;
}

function badge(text, kind) {
  const element = document.createElement("span");
  element.className = `badge badge-${kind}`;
  element.textContent = text;
  return element;
}

function formatDetailValue(value) {
  if (typeof value === "string") {
    return value.replace(/\s+/g, " ").trim();
  }
  if (Array.isArray(value)) {
    return value.map(formatDetailValue).join("; ");
  }
  if (typeof value === "object") {
    if (value.type && value.value) {
      return `${value.type}: ${value.value}`;
    }
    return JSON.stringify(value);
  }
  return String(value);
}

function projectSummary() {
  const project = catalog.project || {};
  const entityCount = Object.keys(catalog.entities || {}).length;
  const relationshipCount = (catalog.relationships || []).length;
  return `${project.title || "Catalog"} - ${entityCount} entities, ${relationshipCount} relationships`;
}

function setStatus(message) {
  document.querySelector("#status").textContent = message;
}
