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
                break;
            case 'misfit':
                this.misfitsNegativeList.push(node)
                break;
            case 'workaround':
                this.workaroundsNegativeList.push(node)
                break;
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

        if(this.rolesNegativeList.length > 0){
            context += `
                Für den betrachteten Prozess wurden bereits folgende Rollen als irrelevant identifiziert:
                [
                ${this.rolesNegativeList.map(w => { return  `"` + w.text + `",`} )}
                ]
                Aus diesem Grund sollten Sie bei der Erstellung einer neuen Rolle darauf achten, dass
                diese sich von denen zuvor genannten unterscheidet.
            `
        }
        return context;
    }

    getMisfitsPromptContext(){
        let context = document.getElementById('additional-context')?.value || '';

        if(this.misfitsNegativeList.length > 0){
            context += `
                Für die betrachtete Rolle wurden bereits folgende Challenges als irrelevant identifziert:
                [
                ${this.misfitsNegativeList.map(w => { return  `"` + w.text + `",`} )}
                ]
                Aus diesem Grund sollten Sie bei der Erstellung einer neuen Challenge darauf achten, dass
                diese 
                    - ein anderes Problem im Prozess beschreibt
                    - andere Ursachen hat 
            `
        }
        return context;
    }
}

export default PromptExtensions