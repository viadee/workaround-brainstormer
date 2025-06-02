class PromptExtensions{

    
    constructor(){
        this.workaroundsNegativeList = []
        this.rolesNegativeList = []
        this.misfitsNegativeList = []
    }

    handleAddNode(node){
        if(!node?.category)
            return;

        switch(node.category){
            case 'role':
                this.rolesNegativeList.push(node)
            case 'misfit':
                this.misfitsNegativeList.push(node)
            case 'workaround':
                this.workaroundsNegativeList.push(node)
        }
    }
    handleRemoveNode(node){
        return;
    }
    getWorkaroundsPromptContext(){
        let context = document.getElementById('additional-context')?.value || '';

        if(this.workaroundsNegativeList.length > 0){
            context += `
            Für den betrachteten Prozess wurden bereits folgende Workarounds als irrelevant identifiziert:
            [
            ${this.workaroundsNegativeList.map(w => { return  `"` + w.text + `",`} )}
            ]
            Aus diesem Grund sollten Sie bei der Erstellung eines neuen Workarounds darauf achten, dass
            dieser  
            - andere Arten von Problemen adressiert, oder
            - andere Ressourcen oder Vorgehensweisen nutzt, oder 
            - andere Vorteile erzielt
            `
        }
        return context;
    }

    getRolesPromptContext(){
        let context = document.getElementById('additional-context')?.value || '';

        if(this.rolesNegativeList > 0){
            context += `
                Für den betrachteten Prozess wurden bereits folgende Rollen generiert:
                [
                ${this.rolesNegativeList.map(w => { return  `"` + w + `",`} )}
                ]
                Aus diesem Grund sollten Sie bei der Erstellung neuer Rollen darauf achten, dass
                diese andere involvierte Rollen wiederspiegeln.
            `
        }
        console.log(context)
        return context;
    }

    getMisfitsPromptContext(){
        let context = document.getElementById('additional-context')?.value || '';

        if(this.misfitsNegativeList.length > 0){
            context += `
                Für die betrachtete Rolle wurden bereits folgende Misfits generiert:
                [
                ${this.misfitsNegativeList.map(w => { return  `"` + w + `",`} )}
                ]
                Aus diesem Grund sollten Sie bei der Erstellung neuer Mitsits darauf achten, dass
                diese andere Arten von Problemen adressiert.
            `
        }
        return context;
    }
}

export default PromptExtensions