export const DIRECTIONS = {up:[0,-1],down:[0,1],left:[-1,0],right:[1,0]};
export class Snake {
  constructor(size=20,random=Math.random){this.size=size;this.random=random;this.reset();}
  reset(){this.body=[[8,10],[7,10],[6,10]];this.direction='right';this.queued=null;this.score=0;this.status='ready';this.placeFood();}
  placeFood(){const free=[];for(let y=0;y<this.size;y++)for(let x=0;x<this.size;x++)if(!this.body.some(p=>p[0]===x&&p[1]===y))free.push([x,y]);this.food=free.length?free[Math.floor(this.random()*free.length)]:null;if(!this.food)this.status='won';}
  turn(direction){if(!DIRECTIONS[direction]||this.queued)return;const a=DIRECTIONS[this.direction],b=DIRECTIONS[direction];if(a[0]+b[0]!==0||a[1]+b[1]!==0)this.queued=direction;}
  step(){if(this.status!=='running')return;this.direction=this.queued||this.direction;this.queued=null;const d=DIRECTIONS[this.direction],head=[this.body[0][0]+d[0],this.body[0][1]+d[1]];const eats=this.food&&head[0]===this.food[0]&&head[1]===this.food[1];const occupied=eats?this.body:this.body.slice(0,-1);if(head.some(v=>v<0||v>=this.size)||occupied.some(p=>p[0]===head[0]&&p[1]===head[1])){this.status='over';return;}this.body.unshift(head);if(eats){this.score+=10;this.placeFood();}else this.body.pop();}
}
