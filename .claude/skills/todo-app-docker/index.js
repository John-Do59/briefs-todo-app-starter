// Skill to manage Docker Compose

export async function execute({ args }) {
  const action = args?.action || "up";
  
  console.log(`Running docker compose ${action}...`);
  
  if (action === "up") {
    await $`cd /Users/amaury/briefs-todo-app-starter && docker compose up --build -d`;
  } else if (action === "down") {
    await $`cd /Users/amaury/briefs-todo-app-starter && docker compose down`;
  } else if (action === "logs") {
    await $`cd /Users/amaury/briefs-todo-app-starter && docker compose logs -f`;
  } else {
    console.log(`Unknown action: ${action}`);
  }
  
  return { success: true };
}
