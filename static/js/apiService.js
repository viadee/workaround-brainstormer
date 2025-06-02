import FileUploadManager from "./fileUpload.js";

class ApiService {

    constructor() {
        this.baseUrl = '/api';
        this.fileUploadManager = new FileUploadManager();
        this.formData = new FormData();
    }

    setFormData(formData) {
        this.formData = formData
    }

    async #post(endpoint) {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            method: 'POST',
            body: this.formData,
        })
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json()

        if (data.error) {
            throw new Error(data.error)
        }

        return data
    }

    async getRoles(additional_context = null, quantity = null) {

        if (additional_context) {
            this.formData.set('additional_context',additional_context)
        }

        if (quantity) {
            this.formData.set('roles_quantity', quantity)
        }

        try {
            const result = await this.#post('/generateRoles')
            return result['roles']
        } catch (error) {
            console.error('Error generating roles:', error)
        }

    }

    async getMisfits(roles, additional_context = null, quantity = null) {

        if (additional_context) {
            this.formData.set('additional_context', additional_context)
        }

        if (quantity) {
            this.formData.set('challenges_quantity', quantity)
        }
        this.formData.set('roles', [roles])

        try {
            return await this.#post('/generateMisfits')
        } catch (error) {
            console.error('Error generating misfits:', error)
        }

    }

    async getWorkarounds(misfit, additional_context = null, quantity = null) {

        if (quantity) {
            this.formData.set('workarounds_quantity', quantity)
        }
        if(additional_context){
            this.formData.set('additional_context', additional_context)
        }
        this.formData.set('misfits', JSON.stringify(misfit))

        try {
            return await this.#post('/generateWorkarounds')
        } catch (error) {
            console.error('Error generating workarounds:', error)
        }
    }

}

export default ApiService;