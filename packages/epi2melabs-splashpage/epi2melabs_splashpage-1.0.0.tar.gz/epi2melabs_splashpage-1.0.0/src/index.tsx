import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { IDocumentManager } from '@jupyterlab/docmanager';

import { MainAreaWidget } from '@jupyterlab/apputils';

import { copyIcon, runIcon } from '@jupyterlab/ui-components';

import { ILauncher } from '@jupyterlab/launcher';

import { Epi2melabsLauncherWidget } from './widget';

import { ITrackedNotebookList, NotebookAction } from './types';

import { labsLogoIcon } from './asset';

const PLUGIN_ID = '@epi2melabs/epi2melabs-splashpage:settings';

const COMMAND = 'create-epi2me-labs-splashpage';

const CATEGORY = 'EPI2ME Labs'


const createLauncherWidget = async (
  sections: ITrackedNotebookList[],
  shell: JupyterFrontEnd.IShell,
  docTrack: IDocumentManager,
  setting: ISettingRegistry.ISettings
): Promise<void> => {
  // Build the widget and add it to the main area
  const content = new Epi2melabsLauncherWidget(setting, docTrack, sections);
  const widget = new MainAreaWidget<Epi2melabsLauncherWidget>({ content });
  widget.title.label = 'EPI2ME Labs';
  shell.add(widget, 'main');
};


const extension: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  requires: [IDocumentManager, ILauncher, ISettingRegistry],
  autoStart: true,
  activate: (
      app: JupyterFrontEnd,
      docTrack: IDocumentManager,
      launcher: ILauncher,
      settings: ISettingRegistry
  ) => {
   const { commands, shell } = app;
   
   Promise.all([app.restored, settings.load(PLUGIN_ID)])
    .then(([, setting]) => {
      // Specify the sections to be shown
      const workdirPath = setting.get('working_dir').composite as string
      const templatePath = setting.get('template_dir').composite as string
      const sections: ITrackedNotebookList[] = [
        {
          name: 'Recent notebooks', 
          tooltip: `Displays notebooks in the ${workdirPath} directory`, 
          path: workdirPath,
          icon: runIcon,
          action: NotebookAction.open
        }, 
        {
          name: 'EPI2ME Labs Templates', 
          tooltip: 'Click on a template to copy it and get started', 
          path: templatePath,
          icon: copyIcon,
          action: NotebookAction.clone
        }
      ]
      createLauncherWidget(sections, shell, docTrack, setting);

      commands.addCommand(COMMAND, {
        caption: 'Create an EPI2ME Labs launcher',
        label: 'EPI2ME Labs',
        icon: args => (args['isPalette'] ? null : labsLogoIcon),
        execute: () => {
         createLauncherWidget(sections, shell, docTrack, setting)
        }
      });
   
      if (launcher) {
        launcher.add({
          command: COMMAND,
          category: CATEGORY
        });
      }
    })
}};

export default extension;
