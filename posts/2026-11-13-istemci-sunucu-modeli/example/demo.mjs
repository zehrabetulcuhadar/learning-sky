import { server } from "./server.mjs";

server.listen(0, async () => {
  process.env.API = `http://localhost:${server.address().port}`;
  await import("./client.mjs");
  server.close();
});
