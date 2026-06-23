const DEFAULT_ROOT_ID = "claim.jesus_created";
const VIEW_STATE_VERSION = 1;

let catalog = null;
let currentRootId = DEFAULT_ROOT_ID;
let expandedPaths = new Set();
let expandedGroupPaths = new Set();
let hiddenGroupPaths = new Set();
let hiddenNodePaths = new Set();
let openHiddenPanels = new Set();
let openHiddenNodePanels = new Set();
let nodeDisplayModes = new Map();
let openQuotePaths = new Set();
let shownBacklinkNodePaths = new Set();
let firstRenderedPathByEntity = new Map();

document.addEventListener("DOMContentLoaded", () => {
  const openButton = document.querySelector("#open-root");
  const copyViewButton = document.querySelector("#copy-view-link");
  const rootInput = document.querySelector("#root-id");

  openButton.addEventListener("click", () => {
    openRoot(rootInput.value);
  });

  copyViewButton.addEventListener("click", () => {
    copyCurrentViewLink();
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
    if (!restoreViewFromHash()) {
      document.querySelector("#root-id").value = initialRoot;
      openRoot(initialRoot, { updateUrl: false });
    }
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
  expandedGroupPaths = new Set();
  hiddenGroupPaths = new Set();
  hiddenNodePaths = new Set();
  openHiddenPanels = new Set();
  openHiddenNodePanels = new Set();
  nodeDisplayModes = new Map();
  openQuotePaths = new Set();
  shownBacklinkNodePaths = new Set();
  document.querySelector("#root-id").value = entityId;

  if (options.updateUrl !== false) {
    const url = new URL(window.location.href);
    url.searchParams.set("root", entityId);
    url.hash = "";
    window.history.replaceState({}, "", url);
  }

  renderTree();
}

async function copyCurrentViewLink() {
  if (!catalog) {
    return;
  }

  const url = new URL(window.location.href);
  url.searchParams.set("root", currentRootId);
  url.hash = `view=${encodeViewState(currentViewState())}`;
  window.history.replaceState({}, "", url);

  try {
    await writeClipboardText(url.toString());
    setStatus("View link copied.");
  } catch (error) {
    setStatus("View link added to the address bar. Copy it from there.");
  }
}

function restoreViewFromHash() {
  const state = viewStateFromHash();
  if (!state || !catalog.entities[state.root]) {
    return false;
  }

  currentRootId = state.root;
  expandedPaths = stringSet(state.expandedPaths);
  expandedGroupPaths = stringSet(state.expandedGroupPaths);
  hiddenGroupPaths = stringSet(state.hiddenGroupPaths);
  hiddenNodePaths = stringSet(state.hiddenNodePaths);
  openHiddenPanels = new Set();
  openHiddenNodePanels = new Set();
  nodeDisplayModes = new Map(stringArray(state.fullNodePaths).map((path) => [path, "full"]));
  openQuotePaths = stringSet(state.openQuotePaths);
  shownBacklinkNodePaths = stringSet(state.shownBacklinkNodePaths);
  document.querySelector("#root-id").value = currentRootId;

  renderTree();
  setStatus("View restored from link.");
  return true;
}

function viewStateFromHash() {
  const hash = window.location.hash.replace(/^#/, "");
  if (!hash) {
    return null;
  }

  const encoded = new URLSearchParams(hash).get("view");
  if (!encoded) {
    return null;
  }

  try {
    const state = decodeViewState(encoded);
    if (state && state.v === VIEW_STATE_VERSION && typeof state.root === "string") {
      return state;
    }
  } catch (error) {
    return null;
  }

  return null;
}

function currentViewState() {
  return {
    v: VIEW_STATE_VERSION,
    root: currentRootId,
    expandedPaths: sortedStrings(expandedPaths),
    expandedGroupPaths: sortedStrings(expandedGroupPaths),
    hiddenGroupPaths: sortedStrings(hiddenGroupPaths),
    hiddenNodePaths: sortedStrings(hiddenNodePaths),
    openQuotePaths: sortedStrings(openQuotePaths),
    shownBacklinkNodePaths: sortedStrings(shownBacklinkNodePaths),
    fullNodePaths: sortedStrings(
      Array.from(nodeDisplayModes.entries())
        .filter((entry) => entry[1] === "full")
        .map((entry) => entry[0]),
    ),
  };
}

function encodeViewState(state) {
  const bytes = new TextEncoder().encode(JSON.stringify(state));
  let binary = "";
  for (const byte of bytes) {
    binary += String.fromCharCode(byte);
  }
  return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

function decodeViewState(encoded) {
  const base64 = encoded.replace(/-/g, "+").replace(/_/g, "/");
  const padded = base64.padEnd(Math.ceil(base64.length / 4) * 4, "=");
  const binary = atob(padded);
  const bytes = Uint8Array.from(binary, (character) => character.charCodeAt(0));
  return JSON.parse(new TextDecoder().decode(bytes));
}

async function writeClipboardText(text) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    await navigator.clipboard.writeText(text);
    return;
  }

  const input = document.createElement("textarea");
  input.value = text;
  input.setAttribute("readonly", "");
  input.className = "clipboard-fallback";
  document.body.appendChild(input);
  input.select();

  try {
    if (!document.execCommand("copy")) {
      throw new Error("copy command failed");
    }
  } finally {
    input.remove();
  }
}

function sortedStrings(values) {
  return Array.from(values).filter((value) => typeof value === "string").sort();
}

function stringArray(values) {
  return Array.isArray(values) ? values.filter((value) => typeof value === "string") : [];
}

function stringSet(values) {
  return new Set(stringArray(values));
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

function renderNode(entityId, path, ancestors, parentRelationship, options = {}) {
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
  const displayMode = nodeDisplayModes.get(path) || "id";
  const quotes = quotesForEntity(entity);
  const shouldShowQuotes = quotes.length > 0 && (displayMode === "full" || openQuotePaths.has(path));
  const groups = relationshipGroups(entityId);
  const hiddenGroups = hiddenRelationshipGroups(path, groups);
  if (displayMode === "id") {
    node.classList.add("node-id-mode");
  }

  node.appendChild(
    renderNodeHeader(entity, path, isExpanded, isRepeated, displayMode, hiddenGroups, options, quotes, shouldShowQuotes)
  );

  if (shouldShowQuotes) {
    node.appendChild(renderQuotes(quotes));
  }

  if (hiddenGroups.length > 0 && openHiddenPanels.has(path)) {
    node.appendChild(renderHiddenGroupsPanel(path, hiddenGroups));
  }

  if (parentRelationship && displayMode === "full") {
    node.appendChild(renderRelationshipSummary(parentRelationship));
  }

  if (displayMode === "full") {
    node.appendChild(renderEntityBody(entity, { omitQuotationFields: shouldShowQuotes }));
  }

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

  if (groups.length === 0) {
    node.appendChild(renderNotice("No related entities."));
    return node;
  }

  const visibleGroups = groups.filter((group) => !isHiddenRelationshipGroup(path, group));
  if (visibleGroups.length === 0) {
    return node;
  }

  const groupsContainer = document.createElement("div");
  groupsContainer.className = "relationship-groups";
  for (const group of visibleGroups) {
    groupsContainer.appendChild(renderRelationshipGroup(group, path, ancestors.concat(entityId)));
  }
  node.appendChild(groupsContainer);

  return node;
}

function renderNodeHeader(
  entity,
  path,
  isExpanded,
  isRepeated,
  displayMode,
  hiddenGroups,
  options,
  quotes,
  shouldShowQuotes,
) {
  const header = document.createElement("header");
  header.className = "node-header";

  const left = document.createElement("div");
  left.className = "node-title-block";

  const titleRow = document.createElement("div");
  titleRow.className = "node-title-row";

  const title = document.createElement(displayMode === "id" ? "p" : "h2");
  title.className = displayMode === "id" ? "entity-id node-id-title" : "";
  title.textContent = displayMode === "id" ? entity.id : entity.label || entity.id;
  titleRow.appendChild(title);

  titleRow.appendChild(badge(entity.kind, "kind"));
  if (entity.perspective && entity.perspective.label) {
    titleRow.appendChild(badge(entity.perspective.label, "perspective"));
  }
  if (isRepeated) {
    titleRow.appendChild(badge("Repeated", "repeated"));
  }

  if (displayMode === "full") {
    const id = document.createElement("p");
    id.className = "entity-id";
    id.textContent = entity.id;
    left.append(titleRow, id);
  } else {
    left.appendChild(titleRow);
  }

  const actions = document.createElement("div");
  actions.className = "node-actions";

  const displayButton = document.createElement("button");
  displayButton.type = "button";
  displayButton.textContent = displayMode === "id" ? "Full" : "ID";
  displayButton.addEventListener("click", () => {
    if (displayMode === "id") {
      nodeDisplayModes.set(path, "full");
    } else {
      nodeDisplayModes.delete(path);
    }
    renderTree();
  });

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

  actions.append(displayButton, toggleButton, rootButton);
  if (displayMode === "id" && quotes.length > 0) {
    const quoteButton = document.createElement("button");
    quoteButton.type = "button";
    quoteButton.textContent = quoteButtonLabel(quotes, shouldShowQuotes);
    quoteButton.setAttribute("aria-expanded", String(shouldShowQuotes));
    quoteButton.addEventListener("click", () => {
      if (openQuotePaths.has(path)) {
        openQuotePaths.delete(path);
      } else {
        openQuotePaths.add(path);
      }
      renderTree();
    });
    actions.insertBefore(quoteButton, toggleButton);
  }
  if (options.canHide) {
    const hideButton = document.createElement("button");
    hideButton.type = "button";
    hideButton.textContent = "Hide";
    hideButton.addEventListener("click", () => {
      hideNodeOccurrence(path);
    });
    actions.appendChild(hideButton);
  }
  if (hiddenGroups.length > 0) {
    const hiddenButton = document.createElement("button");
    hiddenButton.type = "button";
    hiddenButton.textContent = `Hidden ${hiddenGroups.length}`;
    hiddenButton.setAttribute("aria-expanded", String(openHiddenPanels.has(path)));
    hiddenButton.addEventListener("click", () => {
      if (openHiddenPanels.has(path)) {
        openHiddenPanels.delete(path);
      } else {
        openHiddenPanels.add(path);
      }
      renderTree();
    });
    actions.appendChild(hiddenButton);
  }
  header.append(left, actions);
  return header;
}

function renderHiddenGroupsPanel(parentPath, hiddenGroups) {
  const panel = document.createElement("section");
  panel.className = "hidden-groups-panel";

  const heading = document.createElement("h3");
  heading.textContent = "Hidden groups";
  panel.appendChild(heading);

  const list = document.createElement("div");
  list.className = "hidden-groups-list";
  for (const group of hiddenGroups) {
    const groupPath = relationshipGroupPath(parentPath, group);
    const item = document.createElement("div");
    item.className = "hidden-group-item";

    const label = document.createElement("span");
    label.className = "hidden-group-label";
    label.textContent = group.label;
    label.appendChild(badge(String(group.items.length), "count"));

    const showButton = document.createElement("button");
    showButton.type = "button";
    showButton.textContent = "Show";
    showButton.addEventListener("click", () => {
      hiddenGroupPaths.delete(groupPath);
      showDefaultHiddenBacklinks(parentPath, group);
      expandedGroupPaths.delete(groupPath);
      if (hiddenRelationshipGroups(parentPath, relationshipGroupsForPath(parentPath)).length === 0) {
        openHiddenPanels.delete(parentPath);
      }
      renderTree();
    });

    item.append(label, showButton);
    list.appendChild(item);
  }
  panel.appendChild(list);
  return panel;
}

function renderQuotes(quotes) {
  const section = document.createElement("section");
  section.className = "quotes";
  section.setAttribute("aria-label", "Quotations");

  for (const quote of quotes) {
    const figure = document.createElement("figure");
    figure.className = "quote-card";

    const caption = document.createElement("figcaption");
    caption.className = "quote-citation";
    caption.textContent = quoteCitationLabel(quote);

    const blockquote = document.createElement("blockquote");
    blockquote.className = "quote-text";
    blockquote.textContent = quote.quotation;

    figure.append(caption, blockquote);
    section.appendChild(figure);
  }

  return section;
}

function renderHiddenNodesPanel(parentPath, groupPath, hiddenItems) {
  const panel = document.createElement("section");
  panel.className = "hidden-groups-panel hidden-nodes-panel";

  const heading = document.createElement("h3");
  heading.textContent = "Hidden nodes";
  panel.appendChild(heading);

  const list = document.createElement("div");
  list.className = "hidden-groups-list";
  for (const item of hiddenItems) {
    const entity = catalog.entities[item.entityId];
    const itemPath = item.path;
    const row = document.createElement("div");
    row.className = "hidden-group-item";

    const label = document.createElement("span");
    label.className = "hidden-node-label";

    const id = document.createElement("span");
    id.className = "hidden-node-id";
    id.textContent = item.entityId;
    label.appendChild(id);

    if (entity) {
      label.appendChild(badge(entity.kind, "kind"));
      if (entity.perspective && entity.perspective.label) {
        label.appendChild(badge(entity.perspective.label, "perspective"));
      }
    }

    const showButton = document.createElement("button");
    showButton.type = "button";
    showButton.textContent = "Show";
    showButton.addEventListener("click", () => {
      hiddenNodePaths.delete(itemPath);
      if (isDefaultHiddenBacklink(parentPath, item)) {
        shownBacklinkNodePaths.add(itemPath);
      }
      if (hiddenItemsForGroup(parentPath, groupPath, item.group).length === 0) {
        openHiddenNodePanels.delete(groupPath);
      }
      renderTree();
    });

    row.append(label, showButton);
    list.appendChild(row);
  }
  panel.appendChild(list);
  return panel;
}

function renderEntityBody(entity, options = {}) {
  const body = document.createElement("div");
  body.className = "node-body";

  if (entity.summary && entity.summary !== entity.label) {
    const summary = document.createElement("p");
    summary.className = "summary";
    summary.textContent = entity.summary;
    body.appendChild(summary);
  }

  const details = entity.details || {};
  const fields = detailFields(entity.kind, details, options);
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

function detailFields(kind, details, options = {}) {
  if (kind === "evidence") {
    const fields = [];
    if (!options.omitQuotationFields) {
      fields.push(
        { key: "quotation", label: "Quotation" },
        { key: "source_label", label: "Source" },
        { key: "locator", label: "Locator" },
      );
    }
    fields.push({ key: "paraphrase", label: "Paraphrase" });
    return fields;
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

  const groupPath = relationshipGroupPath(parentPath, group);
  const hiddenItems = hiddenItemsForGroup(parentPath, groupPath, group);
  const visibleItems = visibleItemsForGroup(parentPath, groupPath, group);
  const isExpanded = expandedGroupPaths.has(groupPath);
  const isCollapsed = !isExpanded;
  if (isCollapsed) {
    section.classList.add("is-collapsed");
  }

  const header = document.createElement("header");
  header.className = "relationship-group-header";

  const titleRow = document.createElement("div");
  titleRow.className = "relationship-group-title-row";

  const heading = document.createElement("h3");
  heading.textContent = group.label;
  titleRow.appendChild(heading);
  titleRow.appendChild(badge(String(group.items.length), "count"));

  const actions = document.createElement("div");
  actions.className = "relationship-group-actions";

  const toggleButton = document.createElement("button");
  toggleButton.type = "button";
  toggleButton.textContent = isCollapsed ? "Expand" : "Collapse";
  toggleButton.setAttribute("aria-expanded", String(!isCollapsed));
  toggleButton.addEventListener("click", () => {
    if (expandedGroupPaths.has(groupPath)) {
      expandedGroupPaths.delete(groupPath);
    } else {
      expandedGroupPaths.add(groupPath);
    }
    renderTree();
  });

  actions.appendChild(toggleButton);
  if (hiddenItems.length > 0) {
    const hiddenButton = document.createElement("button");
    hiddenButton.type = "button";
    hiddenButton.textContent = `Hidden ${hiddenItems.length}`;
    hiddenButton.setAttribute("aria-expanded", String(openHiddenNodePanels.has(groupPath)));
    hiddenButton.addEventListener("click", () => {
      if (openHiddenNodePanels.has(groupPath)) {
        openHiddenNodePanels.delete(groupPath);
      } else {
        openHiddenNodePanels.add(groupPath);
      }
      renderTree();
    });
    actions.appendChild(hiddenButton);
  }
  if (isCollapsed) {
    const hideButton = document.createElement("button");
    hideButton.type = "button";
    hideButton.textContent = "Hide";
    hideButton.addEventListener("click", () => {
      hiddenGroupPaths.add(groupPath);
      expandedGroupPaths.delete(groupPath);
      renderTree();
    });
    actions.appendChild(hideButton);
  }

  header.append(titleRow, actions);
  section.appendChild(header);

  if (hiddenItems.length > 0 && openHiddenNodePanels.has(groupPath)) {
    section.appendChild(renderHiddenNodesPanel(parentPath, groupPath, hiddenItems));
  }

  if (isCollapsed) {
    return section;
  }

  if (visibleItems.length > 0) {
    const list = document.createElement("div");
    list.className = "children";
    for (const item of visibleItems) {
      list.appendChild(renderNode(item.entityId, item.path, ancestors, item.relationship, { canHide: true }));
    }
    section.appendChild(list);
  }

  return section;
}

function relationshipGroupPath(parentPath, group) {
  return `${parentPath}|group|${group.order}:${group.label}`;
}

function relationshipItemPath(groupPath, item, index) {
  return `${groupPath}|item|${index}:${item.relationship.id}|${item.entityId}`;
}

function hiddenRelationshipGroups(parentPath, groups) {
  return groups.filter((group) => isHiddenRelationshipGroup(parentPath, group));
}

function isHiddenRelationshipGroup(parentPath, group) {
  return (
    hiddenGroupPaths.has(relationshipGroupPath(parentPath, group))
    || isDefaultHiddenBacklinkGroup(parentPath, group)
  );
}

function isDefaultHiddenBacklinkGroup(parentPath, group) {
  const groupPath = relationshipGroupPath(parentPath, group);
  const items = relationshipItemsForGroup(groupPath, group);
  return items.length > 0 && items.every((item) => isDefaultHiddenBacklink(parentPath, item));
}

function visibleItemsForGroup(parentPath, groupPath, group) {
  return relationshipItemsForGroup(groupPath, group).filter(
    (item) => !isHiddenRelationshipItem(parentPath, item),
  );
}

function hiddenItemsForGroup(parentPath, groupPath, group) {
  return relationshipItemsForGroup(groupPath, group).filter(
    (item) => isHiddenRelationshipItem(parentPath, item),
  );
}

function relationshipItemsForGroup(groupPath, group) {
  return group.items.map((item, index) => ({
    ...item,
    group,
    path: relationshipItemPath(groupPath, item, index),
  }));
}

function isHiddenRelationshipItem(parentPath, item) {
  return hiddenNodePaths.has(item.path) || isDefaultHiddenBacklink(parentPath, item);
}

function isDefaultHiddenBacklink(parentPath, item) {
  const parentEntityId = directParentEntityId(parentPath);
  return (
    parentEntityId !== null
    && item.entityId === parentEntityId
    && !shownBacklinkNodePaths.has(item.path)
  );
}

function showDefaultHiddenBacklinks(parentPath, group) {
  const groupPath = relationshipGroupPath(parentPath, group);
  for (const item of relationshipItemsForGroup(groupPath, group)) {
    if (isDefaultHiddenBacklink(parentPath, item)) {
      shownBacklinkNodePaths.add(item.path);
    }
  }
}

function directParentEntityId(path) {
  const groupSeparatorIndex = path.lastIndexOf("|group|");
  if (groupSeparatorIndex === -1) {
    return null;
  }
  return entityIdFromPath(path.slice(0, groupSeparatorIndex));
}

function entityIdFromPath(path) {
  const separatorIndex = path.lastIndexOf("|");
  return separatorIndex === -1 ? path : path.slice(separatorIndex + 1);
}

function hideNodeOccurrence(path) {
  pruneNodeProjectionState(path);
  hiddenNodePaths.add(path);
  renderTree();
}

function pruneNodeProjectionState(path) {
  expandedPaths = pathsWithoutPrefix(expandedPaths, path);
  expandedGroupPaths = pathsWithoutPrefix(expandedGroupPaths, path);
  hiddenGroupPaths = pathsWithoutPrefix(hiddenGroupPaths, path);
  hiddenNodePaths = pathsWithoutPrefix(hiddenNodePaths, path);
  openHiddenPanels = pathsWithoutPrefix(openHiddenPanels, path);
  openHiddenNodePanels = pathsWithoutPrefix(openHiddenNodePanels, path);
  openQuotePaths = pathsWithoutPrefix(openQuotePaths, path);
  shownBacklinkNodePaths = pathsWithoutPrefix(shownBacklinkNodePaths, path);
  nodeDisplayModes = mapWithoutPrefix(nodeDisplayModes, path);
}

function pathsWithoutPrefix(paths, prefix) {
  return new Set(Array.from(paths).filter((path) => !pathMatchesPrefix(path, prefix)));
}

function mapWithoutPrefix(map, prefix) {
  return new Map(Array.from(map.entries()).filter(([path]) => !pathMatchesPrefix(path, prefix)));
}

function pathMatchesPrefix(path, prefix) {
  return path === prefix || path.startsWith(`${prefix}|`);
}

function relationshipGroupsForPath(path) {
  const parts = path.split("|");
  const entityId = parts[parts.length - 1];
  return relationshipGroups(entityId);
}

function quotesForEntity(entity) {
  if (entity.kind === "evidence") {
    return quoteFromEvidence(entity);
  }

  if (entity.kind === "interpretation") {
    return evidenceIdsForInterpretation(entity)
      .map((evidenceId) => catalog.entities[evidenceId])
      .filter((evidence) => evidence && evidence.kind === "evidence")
      .flatMap(quoteFromEvidence);
  }

  return [];
}

function evidenceIdsForInterpretation(entity) {
  const details = entity.details || {};
  return uniqueStrings([
    details.evidence_id,
    ...(Array.isArray(details.evidence_ids) ? details.evidence_ids : []),
    ...(Array.isArray(details.related_evidence_ids) ? details.related_evidence_ids : []),
  ]);
}

function quoteFromEvidence(evidence) {
  const details = evidence.details || {};
  if (typeof details.quotation !== "string" || details.quotation.trim() === "") {
    return [];
  }

  return [
    {
      evidenceId: evidence.id,
      sourceLabel: details.source_short_label || details.source_label || details.source_id || "",
      locator: formatLocatorForCitation(details.locator),
      quotation: details.quotation.trim(),
    },
  ];
}

function uniqueStrings(values) {
  const result = [];
  const seen = new Set();
  for (const value of values) {
    if (typeof value !== "string" || value.trim() === "" || seen.has(value)) {
      continue;
    }
    seen.add(value);
    result.push(value);
  }
  return result;
}

function quoteButtonLabel(quotes, shouldShowQuotes) {
  if (shouldShowQuotes) {
    return quotes.length === 1 ? "Hide Quote" : "Hide Quotes";
  }
  return quotes.length === 1 ? "Quote" : `Quotes ${quotes.length}`;
}

function quoteCitationLabel(quote) {
  return [quote.sourceLabel, quote.locator].filter((value) => value !== "").join(", ");
}

function formatLocatorForCitation(locator) {
  if (locator && typeof locator === "object" && typeof locator.value === "string") {
    return locator.value;
  }
  return typeof locator === "string" ? locator : "";
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
