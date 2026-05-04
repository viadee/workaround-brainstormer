import FileUploadManager from "./fileUpload.js";

class ApiService {

    constructor() {
        this.baseUrl = '/api';
        this.fileUploadManager = new FileUploadManager();
        this.language = "en"

    }

    setFormData(formData) {
        this.formData = formData
    }

    async #post(endpoint) {
        console.log(`[API] POST to ${endpoint}`);
        console.log('[API] FormData contents:', Object.fromEntries(this.formData.entries()));
        
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            method: 'POST',
            body: this.formData,
        })
        
        console.log(`[API] Response status: ${response.status} ${response.statusText}`);
        console.log('[API] Response headers:', Object.fromEntries(response.headers.entries()));
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error(`[API] HTTP error response body: ${errorText}`);
            throw new Error(`HTTP error! status: ${response.status} - ${errorText}`);
        }

        const data = await response.json()
        console.log('[API] Response data type:', typeof data, 'is array:', Array.isArray(data));
        console.log('[API] Response data:', data);
        
        if (data.error) {
            console.error('[API] Backend error:', data.error);
            throw new Error("Error fetching api: " + data.error)
        }
        // flask backend returns [] in llm.py if internal or connection errors occur 
        if(Array.isArray(data) && data.length == 0){
            console.error('[API] Empty array response from backend (likely OpenAI API error or misconfiguration)');
            throw new Error("Error fetching API. This usually occurs due to a connection or internal server error.")
        }
        if(response.headers.get('X-Language') != null){
            this.language = response.headers.get('X-Language')
        }

        return data
    }

    async getRoles(additional_context = null, quantity = 3) {
        console.log('[API] getRoles called with:', { additional_context, quantity });
        
        if (additional_context) {
            this.formData.set('additional_context', additional_context)
        }

        if (quantity) {
            this.formData.set('roles_quantity', quantity)
        }
        
        try {
            const result = await this.#post('/generateRoles');
            console.log('[API] getRoles succeeded');
            return result;
        } catch (error) {
            console.error('[API] getRoles failed:', error);
            throw error;
        }
    }

    async getMisfits(roles, additional_context = null, quantity = 2) {

        if (additional_context) {
            this.formData.set('additional_context', additional_context)
        }

        if (quantity) {
            this.formData.set('challenges_quantity', quantity)
        }
        this.formData.set('roles', [roles])

        return await this.#post('/generateMisfits')


    }

    async getWorkarounds(misfit, additional_context = null, quantity = 2) {

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

    async getSimilarWorkarounds(workaround, additional_context = null, quantity = 2){

        if (quantity) {
            this.formData.set('workarounds_quantity', quantity)
        }
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
     async getManualMisfitNodeLabel(misfit_description){
        if(misfit_description){
            this.formData.set('misfit_description', misfit_description)
        }

        try {
            return await this.#post('/generate_manual_misfit_node_label')
        } catch (error) {
            console.error('Error generating manual misfit label:', error)
        }
    }
}

export default ApiService;