import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  route("people", "pages/people.tsx"),
  route("saved-people", "pages/saved-people.tsx"),
] satisfies RouteConfig;
