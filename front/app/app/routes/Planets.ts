import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  route("planets", "pages/planets.tsx"),
  route("my-planets", "pages/my-planets.tsx"),
] satisfies RouteConfig;
