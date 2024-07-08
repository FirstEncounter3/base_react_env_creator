import subprocess
import shutil
import os
import json

from webpack_data import module_exports

npm_path = shutil.which('npm')
node_path = shutil.which('node')

def check_npm_and_nodejs():
    try:
        print('check npm...')
        subprocess.check_call([npm_path, '--version'])
        print('check node...')
        subprocess.check_call([node_path, '--version'])
        print('check is done!')
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print('check is failed!')
        return False

def make_root_dir():
    try:
        print('create root dir...')
        os.mkdir('root')
        print('create is done!')
        return True
    except FileExistsError:
        print('root dir already exists!')
        return False
    except OSError as e:
        print(f'create is failed: {e}')
        return False

def npm_init():
    try:
        print('init npm...')
        subprocess.check_call([npm_path, 'init', '-y'])
        print('init is done!')
        return True
    except subprocess.CalledProcessError:
        print('init is failed!')
        return False

def npm_install():
    try:
        print('install base dependencies for any project...')
        subprocess.check_call([
            npm_path, 
            'install', 
            '@babel/core', 
            '@babel/preset-env', 
            '@babel/preset-react',
            'babel-loader',
            'css-loader',
            'html-webpack-plugin',
            'react',
            'react-dom',
            'react-router-dom',
            'style-loader',
            'webpack',
            ]
        )
        print('base install is done!')
        subprocess.check_call([
            npm_path,
            'install', 
            'webpack-cli',
            'webpack-dev-server',
            '@types/react-dom',
            '@types/react',
            '--save-dev',
            ]
        )
        print('install is done!')
        return True
    except subprocess.CalledProcessError:
        print('install is failed!')
        return False

def add_scripts_to_package_json():
    print('add scripts to package.json...')
    try:
        with open('package.json', 'r') as f:
            data = json.load(f)
        data['scripts'] = {
            'start': 'webpack-dev-server --open',
            'start-mob': 'webpack-dev-server --open --host 0.0.0.0',
            'build': 'webpack'
        }
        with open('package.json', 'w') as f:
            json.dump(data, f, indent=4)
        print('add is done!')
        return True
    except Exception as e:
        print(f'add is failed: {e}')
        return False

def create_webpack_config():
    print('create webpack.config.js...')
    try:
        with open('webpack.config.js', 'w') as f:
            f.write('const path = require("path");\n')
            f.write('const HtmlWebpackPlugin = require("html-webpack-plugin");\n\n')
            f.write(f'module.exports = {module_exports}')
        print('create is done!')
        return True
    except Exception as e:
        print(f'create is failed: {e}')
        return False

def create_babelrc_file():
    print('create .babelrc file...')
    try:
        with open('.babelrc', 'w') as f:
            f.write('{"presets": ["@babel/preset-env",["@babel/preset-react", {"runtime": "automatic"}]]}')
        print('create is done!')
        return True
    except Exception as e:
        print(f'create is failed: {e}')
        return False

def create_index_js_file():
    print('create index.js file...')
    try:
        with open('index.js', 'w') as f:
            f.write('import { createRoot } from "react-dom/client";\n')
            f.write('import App from "./components/App/App";\n\n')
            f.write('const container = document.getElementById("root");\n')
            f.write('const root = createRoot(container);\n\n')
            f.write('root.render(<App />);')
        print('create is done!')
        return True
    except Exception as e:
        print(f'create is failed: {e}')
        return False

def create_index_html_file():
    print('create index.html file...')
    try:
        with open('index.html', 'w') as f:
            f.write('<!DOCTYPE html>\n')
            f.write('<html lang="en">\n')
            f.write('<head>\n')
            f.write('<meta charset="UTF-8" />\n')
            f.write('<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n')
            f.write('<title>Template</title>\n')
            f.write('</head>\n')
            f.write('<body>\n')
            f.write('<main id="root"></main>\n')
            f.write('<script src="bundle.js"></script>\n')
            f.write('</body>\n')
            f.write('</html>\n')
        print('create is done!')
        return True
    except Exception as e:
        print(f'create is failed: {e}')
        return False

def create_base_app_file():
    print('create base app file...')
    try:
        with open('App.jsx', 'w') as f:
            f.write('import React from "react";\n\n')
            f.write('function App() {return (<div>Hello from base app</div>)}\n\n')
            f.write('export default App;')
        print('create is done!')
        return True
    except Exception as e:
        print(f'create is failed: {e}')
        return False


def main():
    if not check_npm_and_nodejs():
        print('Не установлены npm или node.js')
        exit(1)
    make_root_dir()
    os.chdir('root')
    npm_init()
    npm_install()
    add_scripts_to_package_json()
    create_webpack_config()
    create_babelrc_file()
    os.mkdir('src')
    os.chdir('src')
    os.mkdir('components')
    os.chdir('components')
    os.mkdir('App')
    os.chdir('App')
    create_base_app_file()
    os.chdir('../..')
    create_index_js_file()
    os.chdir('..')
    os.mkdir('public')
    os.chdir('public')
    create_index_html_file()


if __name__ == '__main__':
    main()