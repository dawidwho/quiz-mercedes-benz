import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("pages/home.tsx"),
  route("people", "pages/people.tsx"),
  route("people/:id", "pages/people-detail.tsx"),
  route("planets", "pages/planets.tsx"),
  route("planets/:id", "pages/planets-detail.tsx"),
  route("my-people", "pages/my-people.tsx"),
  route("my-planets", "pages/my-planets.tsx"),
] satisfies RouteConfig;
