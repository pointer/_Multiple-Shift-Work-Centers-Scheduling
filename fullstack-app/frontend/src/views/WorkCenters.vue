&lt;template&gt;
  &lt;v-container&gt;
    &lt;v-row&gt;
      &lt;v-col cols="12"&gt;
        &lt;h2 class="text-h5 mb-4"&gt;Work Center Management&lt;/h2&gt;
        
        &lt;v-dialog v-model="dialog" max-width="800px"&gt;
          &lt;template v-slot:activator="{ props }"&gt;
            &lt;v-btn color="primary" v-bind="props"&gt;Add Work Center&lt;/v-btn&gt;
          &lt;/template&gt;
          
          &lt;v-card&gt;
            &lt;v-card-title&gt;
              &lt;span class="text-h5"&gt;{{ formTitle }}&lt;/span&gt;
            &lt;/v-card-title&gt;
            
            &lt;v-card-text&gt;
              &lt;v-form ref="form"&gt;
                &lt;v-text-field v-model="editedItem.name" label="Work Center Name"&gt;&lt;/v-text-field&gt;
                
                &lt;v-expansion-panels&gt;
                  &lt;v-expansion-panel title="Weekday Demand"&gt;
                    &lt;v-expansion-panel-text&gt;
                      &lt;v-row v-for="level in categoryLevels" :key="'weekday-'+level"&gt;
                        &lt;v-col cols="12" sm="6"&gt;
                          &lt;v-text-field
                            v-model="editedItem.weekday_demand[level]"
                            :label="'Category ' + level + ' Demand'"
                            type="number"
                            min="0"
                          &gt;&lt;/v-text-field&gt;
                        &lt;/v-col&gt;
                      &lt;/v-row&gt;
                    &lt;/v-expansion-panel-text&gt;
                  &lt;/v-expansion-panel&gt;
                  
                  &lt;v-expansion-panel title="Weekend Demand"&gt;
                    &lt;v-expansion-panel-text&gt;
                      &lt;v-row v-for="level in categoryLevels" :key="'weekend-'+level"&gt;
                        &lt;v-col cols="12" sm="6"&gt;
                          &lt;v-text-field
                            v-model="editedItem.weekend_demand[level]"
                            :label="'Category ' + level + ' Demand'"
                            type="number"
                            min="0"
                          &gt;&lt;/v-text-field&gt;
                        &lt;/v-col&gt;
                      &lt;/v-row&gt;
                    &lt;/v-expansion-panel-text&gt;
                  &lt;/v-expansion-panel&gt;
                  
                  &lt;v-expansion-panel title="Available Shifts"&gt;
                    &lt;v-expansion-panel-text&gt;
                      &lt;v-select
                        v-model="editedItem.available_shifts"
                        :items="shifts"
                        label="Available Shifts"
                        multiple
                        chips
                      &gt;&lt;/v-select&gt;
                    &lt;/v-expansion-panel-text&gt;
                  &lt;/v-expansion-panel&gt;
                &lt;/v-expansion-panels&gt;
              &lt;/v-form&gt;
            &lt;/v-card-text&gt;
            
            &lt;v-card-actions&gt;
              &lt;v-spacer&gt;&lt;/v-spacer&gt;
              &lt;v-btn color="error" @click="close"&gt;Cancel&lt;/v-btn&gt;
              &lt;v-btn color="success" @click="save"&gt;Save&lt;/v-btn&gt;
            &lt;/v-card-actions&gt;
          &lt;/v-card&gt;
        &lt;/v-dialog&gt;
      &lt;/v-col&gt;
    &lt;/v-row&gt;
    
    &lt;v-row&gt;
      &lt;v-col cols="12"&gt;
        &lt;v-data-table
          :headers="headers"
          :items="workCenters"
          class="elevation-1"
        &gt;
          &lt;template v-slot:item.actions="{ item }"&gt;
            &lt;v-icon small class="mr-2" @click="editItem(item)"&gt;mdi-pencil&lt;/v-icon&gt;
            &lt;v-icon small @click="deleteItem(item)"&gt;mdi-delete&lt;/v-icon&gt;
          &lt;/template&gt;
        &lt;/v-data-table&gt;
      &lt;/v-col&gt;
    &lt;/v-row&gt;
  &lt;/v-container&gt;
&lt;/template&gt;

&lt;script&gt;
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'WorkCentersView',
  setup() {
    const dialog = ref(false)
    const workCenters = ref([])
    const shifts = ref([])
    const categoryLevels = ref([1, 2, 3, 4, 5])
    
    const editedIndex = ref(-1)
    const editedItem = ref({
      name: '',
      weekday_demand: {},
      weekend_demand: {},
      available_shifts: []
    })
    
    const defaultItem = {
      name: '',
      weekday_demand: {},
      weekend_demand: {},
      available_shifts: []
    }
    
    const headers = [
      { title: 'Name', key: 'name' },
      { title: 'Actions', key: 'actions', sortable: false }
    ]
    
    const fetchWorkCenters = async () => {
      try {
        const response = await axios.get('http://localhost:8000/work-centers/')
        workCenters.value = response.data
      } catch (error) {
        console.error('Error fetching work centers:', error)
      }
    }
    
    const save = async () => {
      try {
        if (editedIndex.value > -1) {
          await axios.put(`http://localhost:8000/work-centers/${editedItem.value.id}`, editedItem.value)
        } else {
          await axios.post('http://localhost:8000/work-centers/', editedItem.value)
        }
        await fetchWorkCenters()
        close()
      } catch (error) {
        console.error('Error saving work center:', error)
      }
    }
    
    const editItem = (item) => {
      editedIndex.value = workCenters.value.indexOf(item)
      editedItem.value = Object.assign({}, item)
      dialog.value = true
    }
    
    const deleteItem = async (item) => {
      if (confirm('Are you sure you want to delete this item?')) {
        try {
          await axios.delete(`http://localhost:8000/work-centers/${item.id}`)
          await fetchWorkCenters()
        } catch (error) {
          console.error('Error deleting work center:', error)
        }
      }
    }
    
    const close = () => {
      dialog.value = false
      editedIndex.value = -1
      editedItem.value = Object.assign({}, defaultItem)
    }
    
    onMounted(async () => {
      await fetchWorkCenters()
      // TODO: Fetch available shifts
    })
    
    return {
      dialog,
      workCenters,
      shifts,
      categoryLevels,
      headers,
      editedItem,
      formTitle: editedIndex.value === -1 ? 'New Work Center' : 'Edit Work Center',
      save,
      editItem,
      deleteItem,
      close
    }
  }
}
&lt;/script&gt;