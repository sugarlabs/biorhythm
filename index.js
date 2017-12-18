const fs = require('fs')
const { promisify } = require('util')
const config = require('./config')

const activityDirectory = 'Biorhythm.activity'
const filesData = config.map(file => ({
  name: file,
  lastModified: 0
}))

const readState = () => {
  for (let file of filesData) {
    fs.stat(file.name, (err, stats) => {
      if (file.lastModified !== 0) {
        if (stats.mtimeMs !== file.lastModified) {
          console.log('Updated File: ', file.name)
          updateFile(file.name)
        }
      }
      file.lastModified = stats.mtimeMs
    })
  }
}
console.log('WATCHING FILES....')
readState()
setInterval(() => {
  readState()
}, 1000)

const updateFile = async file => {
  const readFile = promisify(fs.readFile)
  const writeFile = promisify(fs.writeFile)
  try {
    const data = await readFile(file, 'utf8')
    await writeFile(`/home/sugar/Activities/${activityDirectory}/${file}`, data)
  } catch (err) {
    console.error(err)
  }
}
