import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const api = {
    // Employee endpoints
    async getEmployees() {
        const response = await axios.get(`${API_URL}/employees/`);
        return response.data;
    },

    async createEmployee(employee) {
        const response = await axios.post(`${API_URL}/employees/`, employee);
        return response.data;
    },

    async updateEmployee(id, employee) {
        const response = await axios.put(`${API_URL}/employees/${id}`, employee);
        return response.data;
    },

    async deleteEmployee(id) {
        await axios.delete(`${API_URL}/employees/${id}`);
    },

    // Work Center endpoints
    async getWorkCenters() {
        const response = await axios.get(`${API_URL}/work-centers/`);
        return response.data;
    },

    async createWorkCenter(workCenter) {
        const response = await axios.post(`${API_URL}/work-centers/`, workCenter);
        return response.data;
    },

    async updateWorkCenter(id, workCenter) {
        const response = await axios.put(`${API_URL}/work-centers/${id}`, workCenter);
        return response.data;
    },

    async deleteWorkCenter(id) {
        await axios.delete(`${API_URL}/work-centers/${id}`);
    },

    // Shift endpoints
    async getShifts() {
        const response = await axios.get(`${API_URL}/shifts/`);
        return response.data;
    },

    async createShift(shift) {
        const response = await axios.post(`${API_URL}/shifts/`, shift);
        return response.data;
    },

    // Schedule endpoints
    async getSchedule(workCenterId, startDate, endDate) {
        const response = await axios.get(`${API_URL}/schedule/`, {
            params: {
                work_center_id: workCenterId,
                start_date: startDate,
                end_date: endDate
            }
        });
        return response.data;
    },

    async optimizeWorkforce(workCenterId, startDate, endDate) {
        const response = await axios.post(`${API_URL}/optimize/workforce`, {
            work_center_id: workCenterId,
            start_date: startDate,
            end_date: endDate
        });
        return response.data;
    }
};