import { createRouter, createWebHistory } from 'vue-router';
import industry from '@/components/page/industry.vue';
import details from '@/components/form/trade.vue'
import chart_test from '@/components/charts/chart_test.vue';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes:[
        {path:'/',component:industry},
        {name: 'Details', path:'/details/:pair',component:details},
        {path:'/test/',component:chart_test},
    ],
    linkActiveClass:'active'
});

export default router