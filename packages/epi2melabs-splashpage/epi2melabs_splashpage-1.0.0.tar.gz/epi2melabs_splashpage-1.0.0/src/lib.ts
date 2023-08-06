import { IDocumentManager } from '@jupyterlab/docmanager';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { ITrackedNotebook, NotebookAction } from './types';

import { Contents } from '@jupyterlab/services';

const IPYNB = '.ipynb'


export const actionCallbacks = {
  [NotebookAction.clone]: async (e: string, docTrack: IDocumentManager, settings: ISettingRegistry.ISettings) => {
    await docTrack.copy(e, settings.get('working_dir').composite as string).then(e => {
      docTrack.open(e.path)
    })
  },
  [NotebookAction.open]: (e: string, docTrack: IDocumentManager) => {
    docTrack.open(e)
  }
}

export const getNestedFiles = async (
  path: string,
  docTrack: IDocumentManager,
): Promise<Contents.IModel[]> => {
  return (await Promise.all<Contents.IModel>(
    (await docTrack.services.contents.get(path))
      .content
      .map((Item: Contents.IModel) => {
        return Item.type === 'directory'
          ? getNestedFiles(Item.path, docTrack)
          : Item
      })
  )).flat(Infinity)
}

export const getNotebooks = async (
  path: string,
  docTrack: IDocumentManager,
): Promise<ITrackedNotebook[]> => {
  return (await getNestedFiles(path, docTrack))
    .filter((Item: any) => Item.path.endsWith(IPYNB))
    .map((Item: any): ITrackedNotebook => ({
      name: Item.name,
      path: Item.path,
      last_modified: Item.last_modified
    }));
}