import { createWebHistory, createRouter } from "vue-router"
import HomeStart from "@/views/HomeStart"
import WerteVergleich from "@/views/WerteVergleich"
import ClusteringHere from "@/views/ClusteringHere"
import AnomalieErkennung from "@/views/AnomalieErkennung"

const routes = [
    {
        path: "/",
        name: "Home",
        component: HomeStart, //it's called "component" here but it is actually in views
    },
    {
        path: "/Wertevergleich",
        name: "Wertevergleich",
        component: WerteVergleich,
        alias: "/Wertevergleich",
    },
    {
        path: "/Clustering",
        name: "Clustering",
        component: ClusteringHere,
        alias: "/Clustering",
    },
    {
        path: "/Anomalieerkennung",
        name: "Anomalieerkennung",
        component: AnomalieErkennung,
        alias: "/Anomalieerkennung",
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