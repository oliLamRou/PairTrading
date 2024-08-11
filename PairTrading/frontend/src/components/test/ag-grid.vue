<template>
    test
    <ag-grid-vue
        :rowData="rowData"
        :columnDefs="colDefs"
        style="height: 250px"
        class="ag-theme-quartz"
        @rowClicked="onRowClicked"
        
        :rowSelection="rowSelection"
        :suppressRowClickSelection="false"
    >
    </ag-grid-vue>
    <div> {{ selected.value }}</div>
</template>

<script setup>
    import { ref, reactive, onBeforeMount, watch} from 'vue';
    import axios from 'axios'
    import "ag-grid-community/styles/ag-grid.css"; // Mandatory CSS required by the Data Grid
    import "ag-grid-community/styles/ag-theme-quartz.css"; // Optional Theme applied to the Data Grid
    import { AgGridVue } from "ag-grid-vue3"; // Vue Data Grid Component

    const industries = ref(null);
    const min_price = ref(5);
    const max_price = ref(100);
    const min_volume = ref(1000);
    const max_volume = ref(100000000);

    const rowData = ref(null);

    const selected = reactive({value: "nothing"})

    const fetchIndustries = async () => {
        try {
            const response = await axios.get('http://localhost:5002/get_potential_pair');
            industries.value = response.data;
            console.log(response.data)
        } catch (error) {
            console.error(error);
        }
    };

    const onRowClicked = (value) => {
        console.log("clicked", value.data.industry)
        selected.value = value.data.industry
    }

    const rowSelection = ref(null);

    onBeforeMount(() => {
        //rowSelection.value = "multiple";
        fetchIndustries()
    })

    watch(industries, (newIndustries) => {
        if (newIndustries) {
            rowData.value = newIndustries;
        }
    });

    const colDefs = ref([
        { field: "industry" },
        { field: "potential_pair" },
    ]);

</script>