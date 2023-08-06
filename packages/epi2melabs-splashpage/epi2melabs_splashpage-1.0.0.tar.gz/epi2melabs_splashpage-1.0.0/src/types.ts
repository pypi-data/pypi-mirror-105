import { LabIcon } from "@jupyterlab/ui-components";

export enum NotebookAction {
    open = 'open',
    clone = 'clone',
}

export interface ITrackedNotebook {
    name: string;
    path: string;
    last_modified: string;
    onClick?: (e: string) => void;
}

export interface ITrackedNotebookList {
    path?: string;
    name: string;
    icon: LabIcon;
    tooltip: string;
    action?: NotebookAction;
    notebooks?: ITrackedNotebook[];
}