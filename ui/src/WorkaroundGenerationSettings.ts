import { IWorkaround } from "./types";

export class WorkaroundGenerationSettings{

    private undesirableWorkarounds: Array<IWorkaround>
    
    constructor(){
        this.undesirableWorkarounds = []
    }

    addUndesirableWorkaround(workaround: IWorkaround){
        if(workaround == undefined){
            throw new Error("Undesirable workaround is undefined")
        }
        this.undesirableWorkarounds.push(workaround)
    }
    getUndesired(){
        return this.undesirableWorkarounds;
    }
    getAdditionalPromptContext(){
        let context = (document.getElementById('additional-context') as HTMLInputElement).value || '';

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
}
