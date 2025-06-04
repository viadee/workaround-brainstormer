import FileUploadManager from "./fileUpload.js";

class ApiService {

    constructor() {
        this.baseUrl = '/api';
        this.fileUploadManager = new FileUploadManager();
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
            throw new Error("Error fetching api: " + data.error)
        }
        // flask backend returns [] in llm.py if internal or connection errors occur 
        if(Array.isArray(data) && data.length == 0){
           
            throw new Error("Error fetching API. This usually occurs due to a connection or internal server error.")
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
        return await this.#post('/generateRoles')

    }

    async getMisfits(roles, additional_context = null, quantity = null) {

        if (additional_context) {
            this.formData.set('additional_context', additional_context)
        }

        if (quantity) {
            this.formData.set('challenges_quantity', quantity)
        }
        this.formData.set('roles', [roles])

        return await this.#post('/generateMisfits')


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

    async getSimilarWorkarounds(workaround, additional_context = null){
        if(additional_context){
            this.formData.set('additional_context', additional_context)
        }
        this.formData.set('similar_workaround', JSON.stringify(workaround))

        try {
            return await this.#post('/get_similar_workarounds')
        } catch (error) {
            console.error('Error generating workarounds:', error)
        }
    }
}

export default ApiService;