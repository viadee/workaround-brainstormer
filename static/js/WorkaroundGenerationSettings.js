class WorkaroundGenerationSettings{

    undesirableWorkarounds
    
    constructor(){
        this.undesirableWorkarounds = []
    }

    addUndesirableWorkaround(workaround){
        if(workaround == undefined){
            throw new Error("Undesirable workaround is undefined")
        }
        this.undesirableWorkarounds.push(workaround)
    }
    getUndesired(){
        return this.undesirableWorkarounds;
    }
    getAdditionalPromptContext(){
        let context = document.getElementById('additional-context')?.value || '';

        if(this.undesirableWorkarounds.length > 0){
            context += `
            Für den betrachteten Prozess wurden bereits folgende Workarounds als irrelevant identifiziert:
            [
            ${this.undesirableWorkarounds.map(w => { return  `"` + w.text + `",`} )}
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

    getAdditionalPromptContextAdditionalRoles(generatedRoles){
        let context = document.getElementById('additional-context')?.value || '';

        context += `
            Für den betrachteten Prozess wurden bereits folgende Rollen generiert:
            [
            ${generatedRoles.map(w => { return  `"` + w + `",`} )}
            ]
            Aus diesem Grund sollten Sie bei der Erstellung neuer Rollen darauf achten, dass
            diese andere involvierte Rollen wiederspiegeln.
        `
        console.log(context)
        return context;
    }

    getAdditionalPromptContextAdditionalMisfits(generatedMisfits){
        let context = document.getElementById('additional-context')?.value || '';

        context += `
            Für die betrachtete Rolle wurden bereits folgende Misfits generiert:
            [
            ${generatedMisfits.map(w => { return  `"` + w + `",`} )}
            ]
            Aus diesem Grund sollten Sie bei der Erstellung neuer Mitsits darauf achten, dass
            diese andere Arten von Problemen adressiert.
        `

        return context;
    }
}

export default WorkaroundGenerationSettings