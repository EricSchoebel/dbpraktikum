import { createWebHistory, createRouter } from "vue-router"
import HomeStart from "@/views/HomeStart"
import ProDukte from "@/views/ProDukte"
import KateGorien from "@/views/KateGorien"
import ReViews from "@/views/ReViews"

const routes = [
    {
        path: "/",
        name: "Home",
        component: HomeStart, //it's called "component" here but it is actually in views
    },
    {
        path: "/Produkte",
        name: "Produkte",
        component: ProDukte,
        alias: "/Produkte",
    },
    {
        path: "/Kategorien",
        name: "Kategorien",
        component: KateGorien,
        alias: "/Kategorien",
    },
    {
        path: "/Reviews",
        name: "Reviews",
        component: ReViews,
        alias: "/Reviews",
    },
    {
        path: "/:pathMatch(.*)*",
        redirect: "/",
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
  });
  
  export default router;