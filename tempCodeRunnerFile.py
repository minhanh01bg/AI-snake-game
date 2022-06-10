# bfs_check(snake.get_ass_position(),snake,surface,prev2)
# print(1)
# snake.reload_positions(list_po)
# foodPosition = copy.deepcopy(snake.get_ass_position())
# tePoint = copy.deepcopy(prev2.get(foodPosition))
# path = []
# while foodPosition != snakeHead:
#     path.append(foodPosition)
#     foodPosition = tePoint
#     if foodPosition is None:
#         break
#     # print(foodPosition)
#     tePoint = prev2.get((foodPosition[0], foodPosition[1]))
# path = path[::-1]
# for i in path:
#     drawGrid(surface)
#     for j in path:
#         r = pygame.Rect((j[0], j[1]), (GRIDSIZE, GRIDSIZE))
#         pygame.draw.rect(surface, BFSPath, r)
#     if len(i) != 2:
#         snake.handle(i[2])
#         snake.move()
#     if snake.get_head_position() == food.position:
#         snake.length += 1
#         score += 1
#         food.randomize_position()
#         food.check_position(snake)
#     snake.draw(surface)
#     snake.draw_head(surface)
#     food.draw(surface)
#     screen.blit(surface, (0, 0))
#     text = myfont.render("Score {0}".format(score), 1, (0, 0, 0))
#     screen.blit(text, (5, 10))
#     pygame.display.update()
#     clock.tick(FPS)


if answer == False:
    drawGrid(surface)
    if snake.any_possible_move() == True:
        snake.move()
    snake.draw(surface)
    snake.draw_head(surface)
    food.draw(surface)
    screen.blit(surface, (0, 0))
    text = myfont.render("Score {0}".format(score), 1, (0, 0, 0))
    screen.blit(text, (5, 10))
    pygame.display.update()
    clock.tick(FPS)
    continue