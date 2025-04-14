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
                Folgende sind nicht relevant für den Benutzer und sollten in der Form nicht erneut generiert werden.
            
                ${this.undesirableWorkarounds.map(w => { return w.text + `
                    `} )}
            `
        }
        return context;
    }
}

window.WorkaroundGenerationSettings = WorkaroundGenerationSettings