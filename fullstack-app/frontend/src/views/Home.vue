&lt;template&gt;
  &lt;v-container&gt;
    &lt;v-row&gt;
      &lt;v-col cols="12"&gt;
        &lt;h1 class="text-h3 mb-6"&gt;Multiple Shift Scheduling System&lt;/h1&gt;
      &lt;/v-col&gt;
    &lt;/v-row&gt;

    &lt;v-row&gt;
      &lt;v-col cols="12" md="4"&gt;
        &lt;v-hover v-slot="{ isHovering, props }"&gt;
          &lt;v-card
            v-bind="props"
            :elevation="isHovering ? 8 : 2"
            :class="{ 'on-hover': isHovering }"
          &gt;
            &lt;v-card-title&gt;Employees&lt;/v-card-title&gt;
            &lt;v-card-text&gt;
              &lt;p&gt;Manage employee information, including:&lt;/p&gt;
              &lt;ul&gt;
                &lt;li&gt;Category levels&lt;/li&gt;
                &lt;li&gt;Hourly rates&lt;/li&gt;
                &lt;li&gt;Shift preferences&lt;/li&gt;
              &lt;/ul&gt;
            &lt;/v-card-text&gt;
            &lt;v-card-actions&gt;
              &lt;v-btn color="primary" to="/employees"&gt;Manage Employees&lt;/v-btn&gt;
            &lt;/v-card-actions&gt;
          &lt;/v-card&gt;
        &lt;/v-hover&gt;
      &lt;/v-col&gt;

      &lt;v-col cols="12" md="4"&gt;
        &lt;v-hover v-slot="{ isHovering, props }"&gt;
          &lt;v-card
            v-bind="props"
            :elevation="isHovering ? 8 : 2"
            :class="{ 'on-hover': isHovering }"
          &gt;
            &lt;v-card-title&gt;Work Centers&lt;/v-card-title&gt;
            &lt;v-card-text&gt;
              &lt;p&gt;Configure work centers with:&lt;/p&gt;
              &lt;ul&gt;
                &lt;li&gt;Weekday/weekend demands&lt;/li&gt;
                &lt;li&gt;Category requirements&lt;/li&gt;
                &lt;li&gt;Available shifts&lt;/li&gt;
              &lt;/ul&gt;
            &lt;/v-card-text&gt;
            &lt;v-card-actions&gt;
              &lt;v-btn color="primary" to="/work-centers"&gt;Manage Work Centers&lt;/v-btn&gt;
            &lt;/v-card-actions&gt;
          &lt;/v-card&gt;
        &lt;/v-hover&gt;
      &lt;/v-col&gt;

      &lt;v-col cols="12" md="4"&gt;
        &lt;v-hover v-slot="{ isHovering, props }"&gt;
          &lt;v-card
            v-bind="props"
            :elevation="isHovering ? 8 : 2"
            :class="{ 'on-hover': isHovering }"
          &gt;
            &lt;v-card-title&gt;Schedule&lt;/v-card-title&gt;
            &lt;v-card-text&gt;
              &lt;p&gt;View and optimize schedules:&lt;/p&gt;
              &lt;ul&gt;
                &lt;li&gt;Generate optimal schedules&lt;/li&gt;
                &lt;li&gt;View assignments&lt;/li&gt;
                &lt;li&gt;Analyze costs&lt;/li&gt;
              &lt;/ul&gt;
            &lt;/v-card-text&gt;
            &lt;v-card-actions&gt;
              &lt;v-btn color="primary" to="/schedule"&gt;View Schedule&lt;/v-btn&gt;
            &lt;/v-card-actions&gt;
          &lt;/v-card&gt;
        &lt;/v-hover&gt;
      &lt;/v-col&gt;
    &lt;/v-row&gt;

    &lt;v-row class="mt-6"&gt;
      &lt;v-col cols="12"&gt;
        &lt;v-card&gt;
          &lt;v-card-title&gt;System Statistics&lt;/v-card-title&gt;
          &lt;v-card-text&gt;
            &lt;v-row&gt;
              &lt;v-col cols="12" md="4"&gt;
                &lt;v-skeleton-loader
                  v-if="loading"
                  type="text"
                &gt;&lt;/v-skeleton-loader&gt;
                &lt;div v-else&gt;
                  &lt;div class="text-h6"&gt;{{ stats.employeeCount || 0 }}&lt;/div&gt;
                  &lt;div class="text-subtitle-1"&gt;Total Employees&lt;/div&gt;
                &lt;/div&gt;
              &lt;/v-col&gt;
              &lt;v-col cols="12" md="4"&gt;
                &lt;v-skeleton-loader
                  v-if="loading"
                  type="text"
                &gt;&lt;/v-skeleton-loader&gt;
                &lt;div v-else&gt;
                  &lt;div class="text-h6"&gt;{{ stats.workCenterCount || 0 }}&lt;/div&gt;
                  &lt;div class="text-subtitle-1"&gt;Work Centers&lt;/div&gt;
                &lt;/div&gt;
              &lt;/v-col&gt;
              &lt;v-col cols="12" md="4"&gt;
                &lt;v-skeleton-loader
                  v-if="loading"
                  type="text"
                &gt;&lt;/v-skeleton-loader&gt;
                &lt;div v-else&gt;
                  &lt;div class="text-h6"&gt;{{ stats.scheduledShifts || 0 }}&lt;/div&gt;
                  &lt;div class="text-subtitle-1"&gt;Scheduled Shifts&lt;/div&gt;
                &lt;/div&gt;
              &lt;/v-col&gt;
            &lt;/v-row&gt;
          &lt;/v-card-text&gt;
        &lt;/v-card&gt;
      &lt;/v-col&gt;
    &lt;/v-row&gt;
  &lt;/v-container&gt;
&lt;/template&gt;

&lt;script&gt;
import { ref, onMounted } from 'vue'
import { api } from '../services/api'

export default {
  name: 'HomeView',
  setup() {
    const loading = ref(true)
    const stats = ref({
      employeeCount: 0,
      workCenterCount: 0,
      scheduledShifts: 0
    })

    const fetchStats = async () => {
      try {
        const [employees, workCenters] = await Promise.all([
          api.getEmployees(),
          api.getWorkCenters()
        ])
        
        stats.value = {
          employeeCount: employees.length,
          workCenterCount: workCenters.length,
          scheduledShifts: 0 // TODO: Implement scheduled shifts count
        }
      } catch (error) {
        console.error('Error fetching stats:', error)
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      fetchStats()
    })

    return {
      loading,
      stats
    }
  }
}
&lt;/script&gt;

&lt;style scoped&gt;
.on-hover {
  transition: all 0.3s ease-in-out;
}
&lt;/style&gt;