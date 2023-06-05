const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      { path: "", component: () => import("pages/IndexPage.vue") },

      {
        path: "user-portrait",
        name: "user-portrait",
        component: () => import("src/pages/Portrait"),
      },
      {
        path: "info-input",
        name: "info-input",
        component: () => import("pages/InfoInputPage.vue"),
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
