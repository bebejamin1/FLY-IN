#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   connection.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/17 12:11:27 by bbeaurai            #+#    #+#            #
#   Updated: 2026/04/17 12:23:26 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

class Connection():

    def __init__(self, way_1: object, way_2: object):
        self.max_link_capacity: int = 1
        self.way_1: object = way_1
        self.way_2: object = way_2
