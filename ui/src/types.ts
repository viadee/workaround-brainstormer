import { NodeTypes } from "./nodeTypes"

export interface INode{
    id:number,
    text: string,
    expanded: boolean,
    parent: number
    type?: NodeTypes
    label: string
}

export interface IWorkaround extends INode{

    
    
}