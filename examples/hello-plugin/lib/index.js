/**
 * hello-plugin — 最小可运行示例：注册一个 hello 工具。
 * 三步：定义 Config → 在 apply 里 ctx.tools.register(defineTool(...)) → 导出。
 */
import z from "@deepseek-ai/schemastery";
import { defineTool } from "@deepseek-ai/dsh-tools";

const name = "hello";
const inject = ["tools"];

const Config = z.object({
  greeting: z.string().default("你好，DSH！"),
});

function apply(ctx, config) {
  ctx.tools.register(defineTool({
    name: "hello",
    description: "说一句问候。",
    parameters: {
      who: { type: "string", required: true, description: "向谁问好。" },
    },
    output: {
      schema: {
        type: "object",
        additionalProperties: false,
        required: true,
        properties: {
          message: { type: "string", required: true },
        },
      },
      render: (_args, value) => [{ type: "text", text: value.message }],
    },
    execute: async (args) => ({ message: config.greeting + " " + args.who }),
    presentCall: (args) => ({ card: "generic", title: "hello", kind: "other", rawInput: args }),
  }));
}

export { Config, apply, inject, name };
