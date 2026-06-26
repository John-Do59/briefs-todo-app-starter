// Skill to run Todo App tests

export async function execute() {
  console.log("Running Todo App tests...");
  
  // Run API tests
  console.log("Running API tests...");
  await $`cd /Users/amaury/briefs-todo-app-starter/api && uv sync && uv run pytest tests/ -v`;
  
  // Run frontend tests
  console.log("Running frontend tests...");
  await $`cd /Users/amaury/briefs-todo-app-starter/web && bun install && bun run test`;
  
  console.log("All tests passed!");
  return { success: true };
}
