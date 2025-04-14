&lt;template&gt;
  &lt;v-container&gt;
    &lt;v-row&gt;
      &lt;v-col cols="12"&gt;
        &lt;h2 class="text-h5 mb-4"&gt;Employee Management&lt;/h2&gt;
        
        &lt;v-dialog v-model="dialog" max-width="600px"&gt;
          &lt;template v-slot:activator="{ props }"&gt;
            &lt;v-btn color="primary" v-bind="props" class="mb-4"&gt;
              Add Employee
            &lt;/v-btn&gt;
          &lt;/template&gt;
          
          &lt;v-card&gt;
            &lt;v-card-title&gt;
              &lt;span class="text-h5"&gt;{{ formTitle }}&lt;/span&gt;
            &lt;/v-card-title&gt;
            
            &lt;v-card-text&gt;
              &lt;v-form ref="form"&gt;
                &lt;v-text-field
                  v-model="editedItem.name"
                  label="Name"
                  required
                &gt;&lt;/v-text-field&gt;
                
                &lt;v-select
                  v-model="editedItem.category_level"
                  :items="categoryLevels"
                  label="Category Level"
                  required
                &gt;&lt;/v-select&gt;
                
                &lt;v-text-field
                  v-model="editedItem.hourly_rate"
                  label="Hourly Rate"
                  type="number"
                  prefix="$"
                  required
                &gt;&lt;/v-text-field&gt;
                
                &lt;v-expansion-panels&gt;
                  &lt;v-expansion-panel title="Shift Preferences"&gt;
                    &lt;v-expansion-panel-text&gt;
                      &lt;v-select
                        v-model="editedItem.shift_preferences"
                        :items="shifts"
                        item-title="name"
                        item-value="id"
                        label="Preferred Shifts"
                        multiple
                        chips
                      &gt;&lt;/v-select&gt;
                    &lt;/v-expansion-panel-text&gt;
                  &lt;/v-expansion-panel&gt;
                  
                  &lt;v-expansion-panel title="Work Center Preferences"&gt;
                    &lt;v-expansion-panel-text&gt;
                      &lt;v-select
                        v-model="editedItem.work_center_preferences"
                        :items="workCenters"
                        item-title="name"
                        item-value="id"
                        label="Preferred Work Centers"
                        multiple
                        chips
                      &gt;&lt;/v-select&gt;
                    &lt;/v-expansion-panel-text&gt;
                  &lt;/v-expansion-panel&gt;
                  
                  &lt;v-expansion-panel title="Day Off Preferences"&gt;
                    &lt;v-expansion-panel-text&gt;
                      &lt;v-select
                        v-model="editedItem.day_off_preferences"
                        :items="['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']"
                        label="Preferred Days Off"
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
          :items="employees"
          :loading="loading"
          class="elevation-1"
        &gt;
          &lt;template v-slot:item.actions="{ item }"&gt;
            &lt;v-icon small class="mr-2" @click="editItem(item)"&gt;mdi-pencil&lt;/v-icon&gt;
            &lt;v-icon small @click="deleteItem(item)"&gt;mdi-delete&lt;/v-icon&gt;
          &lt;/template&gt;
          
          &lt;template v-slot:no-data&gt;
            &lt;v-btn color="primary" @click="fetchEmployees"&gt;Reload&lt;/v-btn&gt;
          &lt;/template&gt;
        &lt;/v-data-table&gt;
      &lt;/v-col&gt;
    &lt;/v-row&gt;

    &lt;v-snackbar v-model="snackbar" :color="snackbarColor"&gt;
      {{ snackbarText }}
      &lt;template v-slot:actions&gt;
        &lt;v-btn color="white" text @click="snackbar = false"&gt;Close&lt;/v-btn&gt;
      &lt;/template&gt;
    &lt;/v-snackbar&gt;
  &lt;/v-container&gt;
&lt;/template&gt;

&lt;script&gt;
import { ref, onMounted } from 'vue'
import { api } from '../services/api'

export default {
  name: 'EmployeesView',
  setup() {
    const loading = ref(true)
    const dialog = ref(false)
    const employees = ref([])
    const shifts = ref([])
    const workCenters = ref([])
    const categoryLevels = ref([1, 2, 3, 4, 5])
    
    const snackbar = ref(false)
    const snackbarText = ref('')
    const snackbarColor = ref('success')
    
    const editedIndex = ref(-1)
    const editedItem = ref({
      name: '',
      category_level: 1,
      hourly_rate: 0,
      shift_preferences: [],
      work_center_preferences: [],
      day_off_preferences: []
    })
    
    const defaultItem = {
      name: '',
      category_level: 1,
      hourly_rate: 0,
      shift_preferences: [],
      work_center_preferences: [],
      day_off_preferences: []
    }
    
    const headers = [
      { title: 'Name', key: 'name' },
      { title: 'Category Level', key: 'category_level' },
      { title: 'Hourly Rate', key: 'hourly_rate' },
      { title: 'Actions', key: 'actions', sortable: false }
    ]
    
    const fetchEmployees = async () => {
      loading.value = true
      try {
        const data = await api.getEmployees()
        employees.value = data
      } catch (error) {
        showError('Failed to fetch employees')
        console.error('Error:', error)
      } finally {
        loading.value = false
      }
    }

    const fetchRelatedData = async () => {
      try {
        const [shiftsData, workCentersData] = await Promise.all([
          api.getShifts(),
          api.getWorkCenters()
        ])
        shifts.value = shiftsData
        workCenters.value = workCentersData
      } catch (error) {
        showError('Failed to fetch related data')
        console.error('Error:', error)
      }
    }
    
    const save = async () => {
      try {
        if (editedIndex.value > -1) {
          await api.updateEmployee(editedItem.value.id, editedItem.value)
          showSuccess('Employee updated successfully')
        } else {
          await api.createEmployee(editedItem.value)
          showSuccess('Employee created successfully')
        }
        await fetchEmployees()
        close()
      } catch (error) {
        showError('Error saving employee')
        console.error('Error:', error)
      }
    }
    
    const editItem = (item) => {
      editedIndex.value = employees.value.indexOf(item)
      editedItem.value = Object.assign({}, item)
      dialog.value = true
    }
    
    const deleteItem = async (item) => {
      if (confirm('Are you sure you want to delete this employee?')) {
        try {
          await api.deleteEmployee(item.id)
          showSuccess('Employee deleted successfully')
          await fetchEmployees()
        } catch (error) {
          showError('Error deleting employee')
          console.error('Error:', error)
        }
      }
    }
    
    const close = () => {
      dialog.value = false
      editedIndex.value = -1
      editedItem.value = Object.assign({}, defaultItem)
    }

    const showError = (message) => {
      snackbarText.value = message
      snackbarColor.value = 'error'
      snackbar.value = true
    }

    const showSuccess = (message) => {
      snackbarText.value = message
      snackbarColor.value = 'success'
      snackbar.value = true
    }
    
    onMounted(async () => {
      await Promise.all([fetchEmployees(), fetchRelatedData()])
    })
    
    return {
      dialog,
      loading,
      employees,
      shifts,
      workCenters,
      categoryLevels,
      headers,
      editedItem,
      snackbar,
      snackbarText,
      snackbarColor,
      formTitle: editedIndex.value === -1 ? 'New Employee' : 'Edit Employee',
      save,
      editItem,
      deleteItem,
      close
    }
  }
}
&lt;/script&gt;