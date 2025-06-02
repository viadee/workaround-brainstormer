import FileUploadManager from "./fileUpload.js";
import WorkaroundGenerationSettings from "./WorkaroundGenerationSettings.js";

class ApiService {

    constructor() {
        this.baseUrl = '/api';
        this.fileUploadManager = new FileUploadManager();
        this.workaroundGenerationSettings = new WorkaroundGenerationSettings();
    }

    #setupFormData() {

        const formData = new FormData();

        const description = document.getElementById('process-input').value;
        const additionalContext = document.getElementById('additional-context')?.value || '';

        formData.append('process_description', description);
        formData.append('additional_context', additionalContext);

        const uploadedFile = this.fileUploadManager.getUploadedFile();
        if (uploadedFile) {
            formData.append('file', uploadedFile);
        }

        return formData
    
    }

    async #post(endpoint, formData) {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            method: 'POST',
            body: formData,
        })
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${misfitResponse.status}`);
        }

        const data = await response.json()

        if (data.error) {
            throw new Error(data.error)
        }

        return data
    }

    async getRoles(generatedRoles = null, quantity = null) {

        const formData = this.#setupFormData()


        if (generatedRoles != null) {
            formData.append('additional_context',this.workaroundGenerationSettings.getAdditionalPromptContextAdditionalRoles(generatedRoles))
        }

        if (quantity) {
            formData.append('roles_quantity', quantity)
        }

        try {
            return await this.#post('/generateRoles',formData)
        } catch (error) {
            console.error('Error generating roles:', error)
        }

    }

    async getMisfits(role, generatedMisfits = null, quantity = null) {
        
        const formData = this.#setupFormData()

        if (generatedMisfits) {
            formData.append('additional_context',this.workaroundGenerationSettings.getAdditionalPromptContextAdditionalMisfits(generatedMisfits))
        }

        if (quantity) {
            formData.append('challenges_quantity', quantity)
        }
        formData.append('roles', [role])

        try {
            return this.#post('/generateMisfits', formData)
        } catch (error) {
            console.error('Error generating misfits:', error)
        }

    }

    async getWorkarounds(misfit, quantity = null) {

        const formData = this.#setupFormData()

        if (quantity) {
            formData.append('workarounds_quantity', quantity)
        }
        formData.append('misfits', JSON.stringify(misfit))

        try {
            return this.#post('/generateWorkarounds', formData)
        } catch (error) {
            console.error('Error generating workarounds:', error)
        }
    }

}

export default ApiService;