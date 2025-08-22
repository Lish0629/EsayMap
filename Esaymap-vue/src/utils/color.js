// utils/color.js
export const ColorAdapter = {
  // [r,g,b] -> { r, g, b }
  arrayToObj: (arr) => ({ r: arr[0], g: arr[1], b: arr[2] }),
  // { r, g, b } -> [r,g,b]
  objToArray: (obj) => [obj.r, obj.g, obj.b],
  // [r,g,b] -> #669799
  arrayToHex: (arr) => '#' + arr.map(n => n.toString(16).padStart(2, '0')).join(''),
  // #669799 -> [r,g,b]
  hexToArray: (hex) => {
    const m = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
    return m ? [parseInt(m[1], 16), parseInt(m[2], 16), parseInt(m[3], 16)] : [102, 153, 153]
  }
}