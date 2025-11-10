const { execSync } = require('child_process');
const fs = require('fs');

function render(inputFile, outputFile, width, format) {
    const cmd = `mmdc -i ${inputFile} -o ${outputFile} -w ${width} -f ${format} -c '{"theme": "default"}'`;
    execSync(cmd);
}

if (require.main === module) {
    const [, , inputFile, outputFile, width, format] = process.argv;
    render(inputFile, outputFile, width, format);
}

module.exports = { render };