---
name: playwright-lean
description: Token-efficient Playwright MCP verification and selector discovery using evaluate-first checks. Default to cheap DOM checks, use snapshots only when needed.
metadata: { "openclaw": { "emoji": "🎯" } }
---

# Playwright Lean Skill

## Purpose

Playwright MCP `browser_snapshot` costs 5,000-15,000 tokens per call, while `browser_evaluate` costs 50-200 tokens per call. Replacing snapshot-based checks with evaluate-based checks yields a 96-99% reduction in verification flow token cost. This skill teaches when and how to default to `browser_evaluate` and reserve `browser_snapshot` for rare, justified cases.

## Usage

```
/playwright-lean [url]           # Lean verification mode (default)
/playwright-lean selector [url]  # Selector discovery mode
```

**Default (lean verification)**: Runs evaluate-based state checks with a single evidence screenshot.

**Selector mode**: Extracts all CSS selectors (data-testid, aria-label, id, interactive elements) as structured JSON for selector inventory documentation. Uses `browser_evaluate` instead of `browser_snapshot` for 35-50% token savings with structured output.

Recognition triggers for selector mode: "find selectors", "selector inventory", "what selectors exist", "css selectors", "data-testid list", "discover selectors"

## Core Principle: Evaluate, Don't Snapshot

| Tool | Tokens per call | 5-call flow total | When to use |
|------|------------------|-------------------|-------------|
| `browser_evaluate` | 50-200 | 250-1,000 | Default for state checks: auth, navigation, form submission, table counts |
| `browser_snapshot` | 5,000-15,000 | 25,000-75,000 | Only for first-time selector discovery or unexpected failures where DOM structure is unknown |

## Lean Flow Pattern

1. **navigate** - Use `mcp__playwright__browser_navigate` to reach the target URL.
2. **evaluate-health** - Use `mcp__playwright__browser_wait_for` if needed, then `mcp__playwright__browser_evaluate` with the Page Health snippet to confirm load.
3. **interact** - Use `mcp__playwright__browser_click`, `mcp__playwright__browser_type`, `mcp__playwright__browser_fill_form`, or `mcp__playwright__browser_select_option` to perform the action under test.
4. **evaluate-verify** - Use `mcp__playwright__browser_evaluate` with the most relevant snippet to confirm the outcome.
5. **screenshot** - Use `mcp__playwright__browser_take_screenshot` once for evidence.

## Decision Framework

| Situation | Correct Tool | Reason |
|-----------|-------------|--------|
| "Does the page show an error?" | `browser_evaluate` | Returns specific error text, not full DOM |
| "Is the user authenticated?" | `browser_evaluate` | Auth State snippet returns boolean and username |
| "Did the form submit successfully?" | `browser_evaluate` | Form State snippet checks field values and error states |
| "First time seeing this page - need selectors" | `browser_snapshot` (once only) | Selector discovery requires full DOM |
| "Debugging an unexpected state" | `browser_snapshot` (once only) | Unknown structure requires visual inspection |
| "How many rows are in the table?" | `browser_evaluate` | Table/List State snippet returns row counts and previews |
| "Build selector inventory for documentation" | `browser_evaluate` (Snippet G) | Structured JSON output, 35-50% cheaper than snapshot, ready for docs |

## Seven Reusable JavaScript Snippets

### Snippet A: Page Health (~150 tokens output)

```javascript
(() => ({
  title: document.title,
  url: location.href,
  errorElements: document.querySelectorAll('[class*="error"],[class*="alert"],[role="alert"]').length,
  h1: document.querySelector('h1')?.textContent?.trim() ?? null,
  // Console errors: use mcp__playwright__browser_console_messages tool separately
}))()
```

Returns: page title, URL, count of error-class elements, H1 text. For console error checking, use the `mcp__playwright__browser_console_messages` tool separately.

### Snippet B: Form State (~120 tokens output)

```javascript
((selectors) => {
  const result = {};
  selectors.forEach(sel => {
    const el = document.querySelector(sel);
    result[sel] = el ? { value: el.value, disabled: el.disabled } : null;
  });
  return {
    fields: result,
    validationErrors: [...document.querySelectorAll('[class*="error"]:not([class*="form"])')].map(e => e.textContent?.trim()),
    submitDisabled: document.querySelector('[type="submit"]')?.disabled ?? null
  };
})(['input[name="email"]', 'input[name="password"]'])
```

Returns: field values keyed by selector, validation error text, submit button disabled state. The selectors array is configurable per context.

### Snippet C: Navigation State (~80 tokens output)

```javascript
(() => ({
  url: location.href,
  pathname: location.pathname,
  activeNav: document.querySelector('nav [aria-current="page"], nav .active, nav [class*="active"]')?.textContent?.trim() ?? null,
  breadcrumbs: [...document.querySelectorAll('[aria-label="breadcrumb"] a, .breadcrumb a')].map(a => a.textContent?.trim())
}))()
```

Returns: current URL, pathname, active navigation item text, breadcrumb path array.

### Snippet D: Table/List State (~100 tokens output)

```javascript
(() => {
  const rows = document.querySelectorAll('table tbody tr, [role="row"]:not([role="columnheader"])');
  const pagination = document.querySelector('[aria-label*="pagination"], .pagination, [class*="pagination"]');
  return {
    rowCount: rows.length,
    firstColumnValues: [...rows].slice(0, 5).map(r => r.cells?.[0]?.textContent?.trim() ?? r.querySelector('td, [role="cell"]')?.textContent?.trim()),
    currentPage: pagination?.querySelector('[aria-current="page"], .active')?.textContent?.trim() ?? null,
    totalPages: pagination?.querySelectorAll('li, button, [role="button"]').length ?? null
  };
})()
```

Returns: row count, first-column text for up to 5 rows, current page, total page count.

### Snippet E: Auth State (~60 tokens output)

```javascript
(() => ({
  isLoggedIn: !document.querySelector('[href*="login"], [href*="sign-in"], button[class*="login"]'),
  username: document.querySelector('[data-testid="user-name"], [class*="username"], [class*="user-name"]')?.textContent?.trim() ?? null,
  loginButtonVisible: !!document.querySelector('[href*="login"], [href*="sign-in"]'),
  logoutButtonVisible: !!document.querySelector('[href*="logout"], [href*="sign-out"], button[class*="logout"]')
}))()
```

Returns: boolean `isLoggedIn`, username if present, whether login and logout buttons are visible.

### Snippet F: Visual State (~80 tokens output)

```javascript
((selector) => {
  const el = document.querySelector(selector);
  if (!el) return { found: false };
  const s = getComputedStyle(el);
  const rect = el.getBoundingClientRect?.();
  return {
    found: true,
    display: s.display,
    visibility: s.visibility,
    opacity: s.opacity,
    color: s.color,
    backgroundColor: s.backgroundColor,
    boundingBox: rect?.toJSON?.() ?? null
  };
})('.your-selector-here')
```

Returns: computed display, visibility, opacity, color, background color, and bounding box. Replace `.your-selector-here` with the actual selector.

### Snippet G: Selector Discovery (~200-400 tokens output)

```javascript
(() => {
  const selectors = { byTestId: [], byAriaLabel: [], byId: [], interactive: [] };

  document.querySelectorAll('[data-testid]').forEach(el => {
    selectors.byTestId.push({
      testId: el.dataset.testid,
      tag: el.tagName.toLowerCase(),
      text: (el.textContent || '').trim().slice(0, 30) || null
    });
  });

  document.querySelectorAll('[aria-label]').forEach(el => {
    selectors.byAriaLabel.push({
      label: el.getAttribute('aria-label'),
      tag: el.tagName.toLowerCase()
    });
  });

  document.querySelectorAll('[id]').forEach(el => {
    if (el.id && !el.id.startsWith('__') && !el.id.startsWith('radix') && !el.id.startsWith(':r') && !/^[\u00AB\u00BB]/.test(el.id)) {
      selectors.byId.push({ id: el.id, tag: el.tagName.toLowerCase() });
    }
  });

  document.querySelectorAll('button, a[href], input, select, textarea, [role="button"], [role="tab"], [role="link"]').forEach(el => {
    const bestSelector = el.dataset?.testid ? `[data-testid="${el.dataset.testid}"]` :
                         el.id ? `#${el.id}` :
                         el.getAttribute('aria-label') ? `[aria-label="${el.getAttribute('aria-label')}"]` :
                         null;
    selectors.interactive.push({
      selector: bestSelector,
      tag: el.tagName.toLowerCase(),
      type: el.type || el.getAttribute('role') || (el.tagName === 'A' ? 'link' : null),
      text: (el.textContent || '').trim().slice(0, 30) || null
    });
  });

  return {
    url: location.href,
    counts: {
      testIds: selectors.byTestId.length,
      ariaLabels: selectors.byAriaLabel.length,
      ids: selectors.byId.length,
      interactive: selectors.interactive.length
    },
    selectors
  };
})()
```

Returns: structured selector inventory with counts and categorized selectors. Output is directly usable for creating selector documentation files. Filters out framework-generated IDs (React `__`, Radix `radix`, MUI `:r` prefixes).

**When to use**: Run on each page when building or updating a selector inventory. Replaces `browser_snapshot` for the selector discovery phase of `/verify-frontend` workflows.

## Selector Flow Pattern

For building selector inventories across multiple pages:

1. **navigate** to the target page
2. **evaluate** with the Selector Discovery snippet (Snippet G)
3. **interact** (click a nav link to reach the next page)
4. **evaluate** again with Snippet G on the new page
5. **screenshot** once for evidence after all pages are covered

This pattern costs ~300-400 tokens per page vs ~5,000-15,000 with `browser_snapshot`. For a 10-page app, that's ~3,500 tokens vs ~75,000 -- a 95% reduction.

## Multi-Check Composition

Combine multiple checks into a single `browser_evaluate` call:

```javascript
(() => ({
  health: { title: document.title, errorCount: document.querySelectorAll('[class*="error"]').length },
  auth: { isLoggedIn: !document.querySelector('[href*="login"]'), username: document.querySelector('[class*="username"]')?.textContent?.trim() ?? null },
  nav: { url: location.href, activeNav: document.querySelector('nav [aria-current="page"]')?.textContent?.trim() ?? null }
}))()
```

One `browser_evaluate` call combining three checks costs ~150 tokens. Three separate `browser_snapshot` calls would cost 15,000-45,000 tokens.

## The One-Snapshot Rule

When selectors are unknown (first visit to a page or after a major UI change), ONE `browser_snapshot` is permitted per verification flow.
Agents must document this with an inline comment: `// ONE SNAPSHOT: establishing selector refs`.
After taking the one snapshot and extracting needed selectors, all subsequent checks must use `browser_evaluate`.
Taking a second snapshot in the same flow is an anti-pattern.

## Click via Evaluate

```javascript
document.querySelector('button[data-testid="submit"]')?.click()
```

When the selector is already known, `browser_evaluate` with `.click()` skips the snapshot-to-click-to-snapshot cycle (saves ~10,000-30,000 tokens).

> **Caveat**: `browser_evaluate` with `.click()` bypasses Playwright's built-in actionability checks (visibility, enabled state, stable position). For critical interactions where timing matters, prefer `mcp__playwright__browser_click` which includes built-in actionability waiting. Use evaluate-click only when the element is confirmed present and stable.

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Alternative |
|-------------|---------------|---------------------|
| Snapshot after every navigation | Consumes 5,000-15,000 tokens per page | `browser_evaluate` Navigation State snippet |
| Snapshot to "confirm" a click landed | Visual confirmation not needed for known flows | `browser_evaluate` to check resulting state |
| Snapshot to check auth state on every page | Auth State snippet is 60 tokens vs 15,000 | `browser_evaluate` Auth State snippet |
| Multiple snapshots in one verification flow | Violates One-Snapshot Rule, wastes 10,000-45,000 tokens | Compose snippets into single evaluate call |

## Relationship to Other Skills

| Skill | Relationship | When to Use Instead |
|-------|-------------|---------------------|
| `/playwright-e2e` | Complementary | When authoring test files or full E2E test suites (needs full DOM for test code generation) |
| `/verify-frontend` | Complementary | For full reconnaissance; use `/playwright-lean selector` for lighter-weight selector extraction |
| `/verify-local` | This skill's patterns replace snapshots INSIDE verify-local flows | Use evaluate snippets for state checks within verify-local |
| `/playwright-lean` | This skill | Any state verification where selectors are already known |