import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "My server",
  version: "1.0.0",
});

server.tool("add", { a: z.number(), b: z.number() }, async function ({ a, b }) {
  const sum = a + b;
  return { content: [{ type: "text", text: String(sum) }] };
});

server.tool(
  "weather",
  { city: z.string().describe("Name of the City") },
  async function (city) {
    const result = "32 degreee cel";
    return { content: [{ type: "text", text: String(sum) }] };
  },
);

const transport = new StdioServerTransport();
await server.connect(transport);
console.log("Server is running");
