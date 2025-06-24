import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  route("planets", "pages/planets.tsx"),
  route("saved-planets", "pages/saved-planets.tsx"),
] satisfies RouteConfig;
