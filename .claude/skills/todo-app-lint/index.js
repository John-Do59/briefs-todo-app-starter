// Skill to run Todo App linting

export async function execute() {
  console.log("Running Todo App linting...");
  
  // Run repo-level lint
  console.log("Running repo-level lint...");
  await $`cd /Users/amaury/briefs-todo-app-starter && bun install && bun run lint`;
  
  // Run API lint (ruff)
  console.log("Running API lint...");
  await $`cd /Users/amaury/briefs-todo-app-starter/api && uv sync && uv run ruff check .`;
  
  console.log("Linting complete!");
  return { success: true };
}
