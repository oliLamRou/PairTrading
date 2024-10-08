import { createRouter, createWebHistory } from 'vue-router';
import industry from '@/components/page/industry.vue';
import details from '@/components/page/pair.vue'
import pair_details from '@/components/charts/pair_details.vue'
import chart_test from '@/components/charts/chart_test.vue';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes:[
        {name: 'Industry', path:'/',component:industry},
        {name: 'Details', path:'/details/:pair',component:details},
        {path:'/test/',component:chart_test},
        {path:'/pair_details/',component:pair_details},
    ],
    linkActiveClass:'active'
});

export default router