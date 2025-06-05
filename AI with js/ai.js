import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
import { traceable } from "langsmith/traceable";
import dotenv from "dotenv";
import textToSpechTool from "./audoi.js";

dotenv.config();

const chat = async (message) => {
  // console.log("Ai call happin")
  const llm = await new ChatGoogleGenerativeAI({
    model: "gemini-2.0-flash",
  });
  // console.log("reply is")
  const reply = await llm.invoke(message);
  return reply.content
};

export const tracedChatTool = traceable(chat, {
  name: "chat",
  run_type: "tool",
});

export default tracedChatTool;