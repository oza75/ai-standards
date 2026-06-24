# TypeScript AI Coding Standards

> **Stub** — TypeScript adapter not yet implemented. These standards are
> captured for future use but are not deployed by `ai-standards init`.

## Naming

- Use `camelCase` for variables and functions, `PascalCase` for types, interfaces,
  and classes, `UPPER_SNAKE_CASE` for module-level constants.
- Boolean names start with `is`, `has`, or `can`.

## Typing

- `strict: true` in `tsconfig.json`. No `any` in public interfaces.
- Prefer `unknown` over `any` for values of uncertain type.
- Use `type` for unions and intersections; use `interface` for object shapes
  that may be extended.

## Tests

- Write failing tests first (TDD). Each test asserts one behaviour.
- Use `vitest` or `jest` — be consistent within a project.
- No mocking of internal modules; prefer fakes over mocks.
