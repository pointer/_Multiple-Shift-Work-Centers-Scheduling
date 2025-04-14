&lt;template&gt;
  &lt;v-container&gt;
    &lt;v-row&gt;
      &lt;v-col cols="12"&gt;
        &lt;h2 class="text-h5 mb-4"&gt;Schedule Management&lt;/h2&gt;
      &lt;/v-col&gt;
    &lt;/v-row&gt;

    &lt;v-row&gt;
      &lt;v-col cols="12" md="4"&gt;
        &lt;v-select
          v-model="selectedWorkCenter"
          :items="workCenters"
          item-title="name"
          item-value="id"
          label="Work Center"
          @update:modelValue="fetchSchedule"
        &gt;&lt;/v-select&gt;
      &lt;/v-col&gt;
      
      &lt;v-col cols="12" md="4"&gt;
        &lt;v-date-picker
          v-model="selectedDate"
          range
          @update:modelValue="fetchSchedule"
        &gt;&lt;/v-date-picker&gt;
      &lt;/v-col&gt;
    &lt;/v-row&gt;

    &lt;v-row v-if="scheduleData"&gt;
      &lt;v-col cols="12" md="6"&gt;
        &lt;v-card&gt;
          &lt;v-card-title&gt;Schedule Summary&lt;/v-card-title&gt;
          &lt;v-card-text&gt;
            &lt;v-row&gt;
              &lt;v-col cols="6"&gt;
                &lt;div class="text-subtitle-1"&gt;Total Cost&lt;/div&gt;
                &lt;div class="text-h6"&gt;
                  ${{ formatNumber(scheduleData.summary.total_cost) }}
                &lt;/div&gt;
              &lt;/v-col&gt;
              &lt;v-col cols="6"&gt;
                &lt;div class="text-subtitle-1"&gt;Total Shifts&lt;/div&gt;
                &lt;div class="text-h6"&gt;
                  {{ scheduleData.summary.total_shifts }}
                &lt;/div&gt;
              &lt;/v-col&gt;
              &lt;v-col cols="6"&gt;
                &lt;div class="text-subtitle-1"&gt;Average Daily Cost&lt;/div&gt;
                &lt;div class="text-h6"&gt;
                  ${{ formatNumber(scheduleData.summary.average_daily_cost) }}
                &lt;/div&gt;
              &lt;/v-col&gt;
            &lt;/v-row&gt;

            &lt;v-divider class="my-4"&gt;&lt;/v-divider&gt;

            &lt;div class="text-subtitle-1 mb-2"&gt;Category Utilization&lt;/div&gt;
            &lt;v-progress-linear
              v-for="(utilization, category) in scheduleData.summary.category_utilization"
              :key="category"
              :model-value="utilization"
              :color="getCategoryColor(category)"
              height="25"
              striped
            &gt;
              &lt;template v-slot:default="{ value }"&gt;
                &lt;strong&gt;Category {{ category }}: {{ Math.ceil(value) }}%&lt;/strong&gt;
              &lt;/template&gt;
            &lt;/v-progress-linear&gt;
          &lt;/v-card-text&gt;
        &lt;/v-card&gt;
      &lt;/v-col&gt;

      &lt;v-col cols="12" md="6"&gt;
        &lt;v-card&gt;
          &lt;v-card-title class="d-flex justify-space-between align-center"&gt;
            Daily Cost Trend
          &lt;/v-card-title&gt;
          &lt;v-card-text&gt;
            &lt;v-chart
              class="chart"
              :option="costChartOption"
              autoresize
            /&gt;
          &lt;/v-card-text&gt;
        &lt;/v-card&gt;
      &lt;/v-col&gt;
    &lt;/v-row&gt;

    &lt;v-row&gt;
      &lt;v-col cols="12"&gt;
        &lt;v-card&gt;
          &lt;v-card-title class="d-flex justify-space-between align-center"&gt;
            Schedule
            &lt;v-btn 
              color="primary" 
              @click="optimizeSchedule"
              :loading="optimizing"
            &gt;
              Optimize Schedule
            &lt;/v-btn&gt;
          &lt;/v-card-title&gt;
          
          &lt;v-card-text&gt;
            &lt;v-table v-if="scheduleData"&gt;
              &lt;thead&gt;
                &lt;tr&gt;
                  &lt;th&gt;Date&lt;/th&gt;
                  &lt;th&gt;Shift&lt;/th&gt;
                  &lt;th v-for="level in categoryLevels" :key="level"&gt;
                    Category {{ level }}
                  &lt;/th&gt;
                  &lt;th&gt;Daily Cost&lt;/th&gt;
                &lt;/tr&gt;
              &lt;/thead&gt;
              &lt;tbody&gt;
                &lt;template v-for="(daySchedule, date) in scheduleData.schedule" :key="date"&gt;
                  &lt;tr v-for="shift in daySchedule.shifts" :key="date + shift.id"&gt;
                    &lt;td&gt;{{ formatDate(date) }}&lt;/td&gt;
                    &lt;td&gt;{{ shift.name }} ({{ shift.start_time }}-{{ shift.end_time }})&lt;/td&gt;
                    &lt;td v-for="level in categoryLevels" :key="level"&gt;
                      &lt;v-chip-group&gt;
                        &lt;v-chip
                          v-for="employee in getEmployeesForShift(daySchedule, shift.id, level)"
                          :key="employee.id"
                          size="small"
                          :color="getCategoryColor(level)"
                        &gt;
                          {{ employee.name }}
                        &lt;/v-chip&gt;
                      &lt;/v-chip-group&gt;
                    &lt;/td&gt;
                    &lt;td&gt;
                      ${{ formatNumber(getDailyCost(daySchedule, shift.id)) }}
                    &lt;/td&gt;
                  &lt;/tr&gt;
                &lt;/template&gt;
              &lt;/tbody&gt;
            &lt;/v-table&gt;
            &lt;v-skeleton-loader
              v-else-if="loading"
              type="table"
            &gt;&lt;/v-skeleton-loader&gt;
          &lt;/v-card-text&gt;
        &lt;/v-card&gt;
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
import { ref, computed, onMounted, watch } from 'vue'
import { api } from '../services/api'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import VChart, { THEME_KEY } from 'vue-echarts'
import { format } from 'date-fns'

use([
  CanvasRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

export default {
  name: 'ScheduleView',
  components: {
    VChart
  },
  provide: {
    [THEME_KEY]: 'light'
  },
  setup() {
    const selectedWorkCenter = ref(null)
    const selectedDate = ref([])
    const workCenters = ref([])
    const scheduleData = ref(null)
    const categoryLevels = ref([1, 2, 3, 4, 5])
    const loading = ref(false)
    const optimizing = ref(false)
    
    const snackbar = ref(false)
    const snackbarText = ref('')
    const snackbarColor = ref('success')

    const costChartOption = computed(() => {
      if (!scheduleData.value) return {}

      const dates = Object.keys(scheduleData.value.schedule).sort()
      const costs = dates.map(date => scheduleData.value.schedule[date].daily_cost)

      return {
        title: {
          text: 'Daily Cost Trend'
        },
        tooltip: {
          trigger: 'axis',
          formatter: (params) => {
            const date = params[0].name
            const cost = params[0].value
            return `${date}<br/>Cost: $${formatNumber(cost)}`
          }
        },
        xAxis: {
          type: 'category',
          data: dates.map(date => format(new Date(date), 'MMM dd'))
        },
        yAxis: {
          type: 'value',
          name: 'Cost ($)',
          axisLabel: {
            formatter: (value) => `$${formatNumber(value)}`
          }
        },
        series: [{
          data: costs,
          type: 'line',
          smooth: true,
          name: 'Daily Cost'
        }]
      }
    })

    const fetchWorkCenters = async () => {
      try {
        const response = await api.getWorkCenters()
        workCenters.value = response
      } catch (error) {
        showError('Failed to fetch work centers')
        console.error('Error:', error)
      }
    }

    const fetchSchedule = async () => {
      if (!selectedWorkCenter.value || !selectedDate.value[0] || !selectedDate.value[1]) return
      
      loading.value = true
      try {
        const response = await api.getSchedule(
          selectedWorkCenter.value,
          selectedDate.value[0],
          selectedDate.value[1]
        )
        scheduleData.value = response
      } catch (error) {
        showError('Failed to fetch schedule')
        console.error('Error:', error)
      } finally {
        loading.value = false
      }
    }

    const optimizeSchedule = async () => {
      if (!selectedWorkCenter.value || !selectedDate.value[0] || !selectedDate.value[1]) {
        showError('Please select work center and date range')
        return
      }

      optimizing.value = true
      try {
        await api.optimizeWorkforce(
          selectedWorkCenter.value,
          selectedDate.value[0],
          selectedDate.value[1]
        )
        await fetchSchedule()
        showSuccess('Schedule optimized successfully')
      } catch (error) {
        showError('Failed to optimize schedule')
        console.error('Error:', error)
      } finally {
        optimizing.value = false
      }
    }

    const getEmployeesForShift = (daySchedule, shiftId, categoryLevel) => {
      return daySchedule.employees.filter(emp => 
        emp.shift_id === shiftId && emp.category_level === categoryLevel
      )
    }

    const getDailyCost = (daySchedule, shiftId) => {
      return daySchedule.employees
        .filter(emp => emp.shift_id === shiftId)
        .reduce((sum, emp) => sum + (emp.hourly_rate * 8), 0)
    }

    const formatDate = (dateString) => {
      return format(new Date(dateString), 'MMM dd, yyyy')
    }

    const formatNumber = (value) => {
      return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }).format(value)
    }

    const getCategoryColor = (level) => {
      const colors = {
        1: 'blue',
        2: 'green',
        3: 'amber',
        4: 'orange',
        5: 'red'
      }
      return colors[level] || 'grey'
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
      await fetchWorkCenters()
    })

    watch([selectedWorkCenter, selectedDate], () => {
      if (selectedWorkCenter.value && selectedDate.value.length === 2) {
        fetchSchedule()
      }
    })

    return {
      selectedWorkCenter,
      selectedDate,
      workCenters,
      scheduleData,
      categoryLevels,
      loading,
      optimizing,
      snackbar,
      snackbarText,
      snackbarColor,
      costChartOption,
      fetchSchedule,
      optimizeSchedule,
      getEmployeesForShift,
      getDailyCost,
      formatDate,
      formatNumber,
      getCategoryColor
    }
  }
}
&lt;/script&gt;

&lt;style scoped&gt;
.chart {
  height: 400px;
}
&lt;/style&gt;