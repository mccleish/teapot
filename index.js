

const BACKGROUND = "#101010"
const FOREGROUND = "#50FF50"
const FPS = 144;




console.log(game)
game.width = 800
game.height = 800
const ctx = game.getContext("2d")
console.log(ctx)

function clear(){
ctx.fillStyle = BACKGROUND
ctx.fillRect(0, 0, game.width, game.height)
}

function point({x,y}){
    const s = 20;
ctx.fillStyle = FOREGROUND
ctx.fillRect(x - s/2, y - s/2, s, s)
}

function line(p1, p2){
    ctx.strokeStyle = FOREGROUND;
    ctx.lineWidth = 1;
    ctx.beginPath();

    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p2.x, p2.y);
    ctx.stroke();
}
function screen(p){
    // -1 to 1 --> 0 to w or h
    x=(p.x + 1)/2*game.width
   y= (1- (p.y + 1)/2)*game.height

   return {x,y}

}


function project({x,y,z}){
return {
        x: x/z,
        y: y/z,
    }

}



let dz=1;
let theta = 0;




function translate_z({x,y,z}, dz){ // move z away / closer by dz

    return {x,y, z: z + dz};
}

function rotate_xz({x,y,z}, theta){

    return{
        x: x * Math.cos(theta) - z*Math.sin(theta),
        y,
        z: x * Math.sin(theta) + z*Math.cos(theta),


    }

}
/*
const vs = [
    {x:0.25, y:0.25, z:0.25},
    {x:0.25, y:-0.25, z:0.25},
    {x:-0.25, y:-0.25, z:0.25},
    {x:-0.25, y:0.25, z:0.25}, 

    {x:0.25, y:0.25, z:-0.25},
    {x:0.25, y:-0.25, z:-0.25},
    {x:-0.25, y:-0.25, z:-0.25},
    {x:-0.25, y:0.25, z:-0.25}, 

]

const fs = [

    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [0,4],
    [1,5],
    [2,6],
    [3,7],

]
*/

function frame(){ 
    const dt = 1/FPS;
    //dz += dt
    theta += 2*Math.PI *dt;
    clear()
    for (const v of vs){
        //point(screen(project(translate_z(rotate_xz(v, theta), dz))))
    }
    for (const f of fs){

        for (let i = 0; i < f.length; ++i){
            const a = vs[f[i]];
            const b = vs[f[(i+1)%f.length]];
            line(screen(project(translate_z(rotate_xz(a, theta), dz)))
            ,screen(project(translate_z(rotate_xz(b, theta), dz))))
        }

    }
    
    setTimeout(frame, 1000/FPS);
}
setTimeout(frame, 1000/FPS);

