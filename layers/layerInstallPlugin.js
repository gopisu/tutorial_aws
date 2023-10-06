'use strict';
const shell = require('shelljs');

class LayerInstallPlugin {
  constructor(serverless) {
    this.serverless = serverless;
    this.hooks = {
      'package:initialize': () => this.beforePackage(),
    };
  }

  beforePackage() {
    const files = shell.find('layers').filter(function (file) {
      return file.includes('requirements.txt');
    });
    const dirs = files.map((file) => file.split('/requirements.txt')[0]);
    const architecture = this.serverless.configurationInput.provider.architecture === 'x86_64' ? 'x86_64' : 'aarch64';
    dirs.forEach(dir => {
      shell.cd(dir)
      shell.exec('rm -rf python');
      shell.exec(`pip install -t python/lib/site-packages -r requirements.txt --platform=manylinux2014_${architecture} --only-binary=:all:`);
      shell.cd('../../');
    })
  }

}

module.exports = LayerInstallPlugin;
