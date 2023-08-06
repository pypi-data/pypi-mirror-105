import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * A plugin for Oxford Nanopore Technologies/epi2melabs-theme
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: '@epi2melabs/epi2melabs-theme:plugin',
  requires: [IThemeManager],
  activate: function(app: JupyterFrontEnd, manager: IThemeManager) {
    const style = '@epi2melabs/epi2melabs-theme/index.css';

    manager.register({
      name: 'epi2melabs-theme',
      isLight: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  },
  autoStart: true
};

export default plugin;
