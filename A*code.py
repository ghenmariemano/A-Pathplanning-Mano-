import pygame
from queue import PriorityQueue

class Take:
	def __init__(show, x, y, wid, trow):
		show.row = x
		show.col = y
		show.width = wid
		show.x = x * wid
		show.y = y * wid
		show.neighbors = []
		show.total_rows = trow
		show.color = (255, 255, 255)

	def error(err):
		return err.color == (51, 51, 51)

	def sides(self, box):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not box[self.row + 1][self.col].error():
			self.neighbors.append(box[self.row + 1][self.col])

		if self.row > 0 and not box[self.row - 1][self.col].error():
			self.neighbors.append(box[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not box[self.row][self.col + 1].error():
			self.neighbors.append(box[self.row][self.col + 1])

		if self.col > 0 and not box[self.row][self.col - 1].error():
			self.neighbors.append(box[self.row][self.col - 1])

	def position(pos):
		return pos.row, pos.col

	def cant(ca):
		return ca.row, ca.col

	def can(c):
		return c.row, c.col

	def reset(res):
		res.color = (255, 255, 255)

	def start(sta):
		sta.color = (153, 153 ,255)

	def end(e):
		e.color = (255, 128, 128)

	def path(pat):
		pat.color = (153,51,102)

	def barrier(bar):
		bar.color = (51, 51, 51)

	def draw(n, st):
		pygame.draw.rect(st, n.color, (n.x, n.y, n.width, n.width))

def algo(draw, grid, x, y):
	cnt = 0
	set = PriorityQueue()
	set.put((0, cnt, x))
	cfrom = {}
	xtrace = {spot: float("inf") for row in grid for spot in row}
	xtrace[x] = 0
	yend = {spot: float("inf") for row in grid for spot in row}
	def point(p1, p2):
		x1, y1 = p1
		x2, y2 = p2
		return abs(x1 - x2) + abs(y1 - y2)
	yend[x] = point(x.position(), y.position())

	startx = {x}

	while not set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		state = set.get()[2]
		startx.remove(state)

		if state == y:
			def depath(cfrom, at, go):
				while at in cfrom:
					at = cfrom[at]
					at.path()
					go()
			depath(cfrom, y, draw)
			y.end()
			return True

		for next in state.neighbors:
			temp_g_score = xtrace[state] + 1

			if temp_g_score < xtrace[next]:
				cfrom[next] = state
				xtrace[next] = temp_g_score
				yend[next] = temp_g_score + point(next.position(), y.position())

				if next not in startx:
					cnt += 1
					set.put((yend[next], cnt, next))
					startx.add(next)
					next.can()

		draw()

		if state != x:
			state.cant()

	return False

def drawG(line, length):
	grid = []
	gap = length // line
	for i in range(line):
		grid.append([])
		for j in range(line):
			spot = Take(i, j, gap, line)
			grid[i].append(spot)

	return grid

def draw(cube, grid, linexy, lengthxy):

	cube.fill((255, 255, 255))
	for row in grid:
		for spot in row:
			spot.draw(cube)

	def grids(cen, r, w):
		gap = w // r
		for i in range(r):
			pygame.draw.line(cen, (150, 150, 150), (0, i * gap), (w, i * gap))
		for j in range(r):
			pygame.draw.line(cen, (150, 150, 150), (j * gap, 0), (j * gap, w))

	grids(cube, linexy, lengthxy)
	pygame.display.update()

def this(lin, width):
	sides = 10
	grid = drawG(sides, width)

	start = None
	end = None

	run = True
	while run:
		draw(lin, grid, sides, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			def spos(ps, rows, width):
				gap = width // rows
				y, x = ps

				row = y // gap
				col = x // gap

				return row, col

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = spos(pos, sides, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.start()

				elif not end and spot != start:
					end = spot
					end.end()

				elif spot != end and spot != start:
					spot.barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = spos(pos, sides, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_TAB and start and end:
					for row in grid:
						for spot in row:
							spot.sides(grid)

					algo(lambda: draw(lin, grid, sides, width), grid, start, end)

				if event.key == pygame.K_ESCAPE:
					start = None
					end = None
					grid = drawG(sides, width)

	pygame.quit()

size = 500
get = pygame.display.set_mode((size,size))
pygame.display.set_caption("A* Pathfinding")

this(get,size)
