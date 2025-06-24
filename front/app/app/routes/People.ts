import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  route("people", "pages/people.tsx"),
  route("my-people", "pages/my-people.tsx"),
] satisfies RouteConfig;
