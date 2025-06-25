import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("pages/home.tsx"),
  route("people", "pages/people.tsx"),
  route("people/:id", "pages/people-detail.tsx"),
  route("people/:id/edit", "pages/people-edit.tsx"),
  route("people-insights", "pages/people-insights.tsx"),
  route("planets", "pages/planets.tsx"),
  route("planets/:id", "pages/planets-detail.tsx"),
  route("planets/:id/edit", "pages/planets-edit.tsx"),
  route("planets-insights", "pages/planets-insights.tsx"),
] satisfies RouteConfig;
