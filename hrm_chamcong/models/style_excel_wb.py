# coding=utf-8
def get_style(wb):
    style_7_right_border = wb.add_format({
        'bold': False,
        'font_size': '7',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_7_left = wb.add_format({
        'bold': False,
        'font_size': '7',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_7_bold_left = wb.add_format({
        'bold': True,
        'font_size': '7',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True
    })

    style_7_bold_center = wb.add_format({
        'bold': True,
        'font_size': '7',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True
    })

    style_7_bold_right = wb.add_format({
        'bold': True,
        'font_size': '7',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
    })

    style_7_left_border = wb.add_format({
        'bold': False,
        'font_size': '7',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_7_center = wb.add_format({
        'bold': False,
        'font_size': '7',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_7_center_italic = wb.add_format({
        'bold': False,
        'font_size': '7',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True, 'italic': True,
        'border': False
    })

    style_7_center_border = wb.add_format({
        'bold': False,
        'font_size': '7',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_7_bold_center_border = wb.add_format({
        'bold': True,
        'font_size': '7',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_8_right_border = wb.add_format({
        'bold': False,
        'font_size': '8',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_8_left = wb.add_format({
        'bold': False,
        'font_size': '8',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_8_left_no_text_wrap = wb.add_format({
        'bold': False,
        'font_size': '8',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': False,
        'border': False
    })

    style_8_left_number = wb.add_format({
        'bold': False,
        'font_size': '8',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'num_format': '#,###',
        'text_wrap': True,
        'border': False
    })

    style_8_right_number = wb.add_format({
        'bold': False,
        'font_size': '8',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'num_format': '#,###',
        'text_wrap': True,
        'border': False
    })
    style_8_right_number_border = wb.add_format({
        'bold': False,
        'font_size': '8',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'num_format': '#,###',
        'text_wrap': True,
        'border': True
    })

    style_8_left_border = wb.add_format({
        'bold': False,
        'font_size': '8',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_8_center = wb.add_format({
        'bold': False,
        'font_size': '8',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_8_center_italic = wb.add_format({
        'bold': False,
        'font_size': '8',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True, 'italic': True,
        'border': False
    })

    style_8_center_italic_bold = wb.add_format({
        'bold': True,
        'font_size': '8',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True, 'italic': True,
        'border': False
    })

    style_8_center_italic_bold_border = wb.add_format({
        'bold': True,
        'font_size': '8',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True, 'italic': True,
        'border': True
    })

    style_8_center_italic_bold_border_color = wb.add_format({
        'bold': True,
        'font_size': '8',
        'font_color': 'black',
        'bg_color': '#a1bfd9',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True, 'italic': True,
        'border': True
    })

    style_8_center_border = wb.add_format({
        'bold': False,
        'font_size': '8',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_8_bold_center_border = wb.add_format({
        'bold': True,
        'font_size': '8',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_8_bold_left = wb.add_format({
        'bold': True,
        'font_size': '8',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_8_bold_right = wb.add_format({
        'bold': True,
        'font_size': '8',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_8_bold_center = wb.add_format({
        'bold': True,
        'font_size': '8',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_8_bold_left_border = wb.add_format({
        'bold': True,
        'font_size': '8',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_8_bold_right_border = wb.add_format({
        'bold': True,
        'font_size': '8',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_8_bold_right_border_number = wb.add_format({
        'bold': True,
        'font_size': '8',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'num_format': '#,###',
        'text_wrap': True,
        'border': True
    })

    style_8_left_bold_no_border = wb.add_format({
        'bold': True,
        'font_size': '8',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': False,
    })

    style_9_bold_center_border = wb.add_format({
        'bold': True,
        'font_size': '9',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_9_bold_right_border = wb.add_format({
        'bold': True,
        'font_size': '9',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_9_bold_right_border_italic = wb.add_format({
        'bold': True,
        'font_size': '9',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'italic': True,
        'border': True
    })

    style_9_bold_left_border = wb.add_format({
        'bold': True,
        'font_size': '9',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_9_bold_left_border_red = wb.add_format({
        'bold': True,
        'font_size': '9',
        'font_color': 'red',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_9_right_border = wb.add_format({
        'bold': False,
        'font_size': '9',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'num_format': '#,##0.00',
    })

    style_9_left_border = wb.add_format({
        'bold': False,
        'font_size': '9',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_9_center_border = wb.add_format({
        'bold': False,
        'font_size': '9',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_9_bold_center_border_rotation = wb.add_format({
        'bold': True,
        'font_size': '9',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'rotation': 90,
    })

    style_9_center_border_rotation = wb.add_format({
        'bold': False,
        'font_size': '9',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'rotation': 90,
    })

    style_9_center_border_italic = wb.add_format({
        'bold': False,
        'font_size': '9',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'italic': True
    })

    style_9_left_border_italic = wb.add_format({
        'bold': False,
        'font_size': '9',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'italic': True
    })

    style_9_bold_left_top_border_diag = wb.add_format({
        'bold': True,
        'font_size': '9',
        'font_color': 'black',
        'align': 'left',
        'valign': 'top',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'diag_type': 2
    })

    style_9_bold_center_border_italic = wb.add_format({
        'bold': True,
        'font_size': '9',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'italic': True
    })

    style_9_bold_center = wb.add_format({
        'bold': True,
        'font_size': '9',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True
    })

    style_9_left = wb.add_format({
        'font_size': '9',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True
    })

    style_9_bold_left = wb.add_format({
        'bold': True,
        'font_size': '9',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True
    })

    style_9_right_border_italic = wb.add_format({
        'bold': False,
        'font_size': '9',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'italic': True
    })
    style_9_bold_center_wrap_border = wb.add_format({
        'bold': True,
        'font_size': '9',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'italic': False
    })
    style_9_center_wrap_border = wb.add_format({
        'bold': False,
        'font_size': '9',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'italic': False
    })
    style_9_left_wrap_border = wb.add_format({
        'bold': False,
        'font_size': '9',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'italic': False
    })

    style_9_left_italic = wb.add_format({
        'font_size': '9',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'italic': True
    })

    style_9_center_border_top_italic = wb.add_format({
        'bold': True,
        'font_size': '9',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'top': True,
        'bottom': 0,
        'left': True,
        'right': True,
        'italic': False
    })

    style_9_center_border_bottom_italic = wb.add_format({
        'bold': False,
        'font_size': '9',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'top': 0,
        'bottom': True,
        'left': True,
        'right': True,
        'italic': True
    })

    style_9_bold_center_border_continuous = wb.add_format({
        'bold': True,
        'font_size': '9',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'bottom': 7,
        'top': 0,
        'left': True,
        'right': True
    })

    style_9_bold_left_border_continuous = wb.add_format({
        'bold': True,
        'font_size': '9',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'bottom': 7,
        'top': 0,
        'left': True,
        'right': True
    })

    style_9_bold_right_border_continuous = wb.add_format({
        'bold': True,
        'font_size': '9',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'bottom': 7,
        'top': 0,
        'left': True,
        'right': True
    })

    style_9_center_border_continuous = wb.add_format({
        'bold': False,
        'font_size': '9',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'bottom': 7,
        'top': 0,
        'left': True,
        'right': True
    })

    style_9_left_border_continuous = wb.add_format({
        'bold': False,
        'font_size': '9',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'bottom': 7,
        'top': 0,
        'left': True,
        'right': True
    })

    style_9_right_border_continuous = wb.add_format({
        'bold': False,
        'font_size': '9',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'bottom': 7,
        'top': 0,
        'left': True,
        'right': True
    })

    style_10_bold_center_border = wb.add_format({
        'bold': True,
        'font_size': '10',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_10_bold_right_border = wb.add_format({
        'bold': True,
        'font_size': '10',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_10_bold_right_border_italic = wb.add_format({
        'bold': True,
        'font_size': '10',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'italic': True,
        'border': True
    })

    style_10_bold_left_border = wb.add_format({
        'bold': True,
        'font_size': '10',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_10_bold_left_border_bottom = wb.add_format({
        'bold': True,
        'font_size': '10',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'bottom': True
    })

    style_10_bold_left_border_red = wb.add_format({
        'bold': True,
        'font_size': '10',
        'font_color': 'red',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_10_bold_center_border_red = wb.add_format({
        'bold': True,
        'font_size': '10',
        'font_color': 'red',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_10_right_border = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_10_left_border = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_10_left_border_bottom = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'bottom': True
    })

    style_10_center_border = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_10_center_border_red = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'red',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_10_left_border_red = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'red',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_10_center_italic = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'italic': True,
        'border': False
    })

    style_10_center_italic_border = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'italic': True,
        'border': True
    })

    style_10_left_italic = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'italic': True,
        'border': False
    })

    style_10_left_italic_border = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'italic': True,
        'border': True
    })

    style_10_bold_left_italic = wb.add_format({
        'bold': True,
        'font_size': '10',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'italic': True,
        'border': False
    })

    style_10_right_italic = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'italic': True,
        'border': False
    })

    style_10_bold_center_border_rotation = wb.add_format({
        'bold': True,
        'font_size': '10',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'rotation': -90,
    })

    style_10_center_border_rotation = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'rotation': 90,
    })

    style_10_center_border_rotation_red = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'red',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'rotation': 90,
    })

    style_12_bold_center_border_rotation = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'rotation': 90,
    })

    style_12_italic_center_wrap = wb.add_format(
        {
            'font_size': '12',
            'font_color': 'black',
            'align': 'center',
            'valign': 'vcenter',
            'font_name': 'Times New Roman',
            'text_wrap': True,
            'italic': True,
        }
    )

    style_12_italic_left_wrap = wb.add_format(
        {
            'font_size': '12',
            'font_color': 'black',
            'align': 'left',
            'valign': 'vcenter',
            'font_name': 'Times New Roman',
            'text_wrap': True,
            'italic': True,
        }
    )

    style_12_center_border_rotation = wb.add_format({
        'bold': False,
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'rotation': 90,
    })
    style_11_center_italic_border = wb.add_format({
        'italic': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': False,
        'border': True
    })

    style_10_center_border_italic = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'italic': True
    })

    style_10_left_border_italic = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'italic': True
    })

    style_10_bold_left_top_border_diag = wb.add_format({
        'bold': True,
        'font_size': '10',
        'font_color': 'black',
        'align': 'left',
        'valign': 'top',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'diag_type': 2
    })

    style_10_bold_center_border_italic = wb.add_format({
        'bold': True,
        'font_size': '10',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'italic': True
    })

    style_10_left = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': False,
        'border': False
    })

    style_10_left_red = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'red',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': False,
        'border': False
    })

    style_10_right = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': False,
        'border': False
    })

    style_10_center = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': False,
        'border': False
    })

    style_10_bold_left = wb.add_format({
        'bold': True,
        'font_size': '10',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': False,
        'border': False
    })

    style_10_bold_right = wb.add_format({
        'bold': True,
        'font_size': '10',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': False,
        'border': False
    })

    style_10_bold_center = wb.add_format({
        'bold': True,
        'font_size': '10',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': False,
        'border': False
    })

    style_10_right_bold_border_money = wb.add_format({
        'bold': True,
        'font_size': '10',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#,###',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_10_right_bold_border_number = wb.add_format({
        'bold': True,
        'font_size': '10',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_10_right_italic_border_number = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'italic': True
    })

    style_10_right_border_money = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#,###',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_10_right_italic_border_money = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#,###',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'italic': True
    })

    style_10_right_border_number = wb.add_format({
        'bold': False,
        'font_size': '10',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_left = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_11_center = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_11_center_border = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_center_bold_border = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_center_border_number = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'num_format': '#,###',
        'border': True
    })

    style_11_center_bold_border_number = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'num_format': '#,###',
        'border': True
    })

    style_11_bold_center_underline = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'underline': True
    })

    style_11_bold_center_border = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_bold_left = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True
    })

    style_11_bold_left_border = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_bold_right_border = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_bold_right = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
    })

    style_11_left_border = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_left_wrap_border = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_bold_left_wrap_border = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })
    style_11_bold_center_wrap_border = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })
    style_11_center_wrap_border = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_middle_wrap_border = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'middle',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_left_bold = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': False,
        'bottom': True, 'top': True
    })

    style_11_center_bold = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': False
    })

    style_11_center_italic = wb.add_format({
        'italic': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': False
    })

    style_11_center_italic_bold = wb.add_format({
        'italic': True,
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': False
    })

    style_11_left_bold_no_border = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': False,
    })

    style_11_left_bold_number = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'num_format': '#0.00;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': False,
    })

    style_11_left_border_right = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'right': True,
        'bottom': True,
        'top': True,
        'text_wrap': True,
    })

    style_11_right_border_number = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#,###',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_center_border_number_no_digit = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'num_format': '#;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_center_border_number_1digit = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'num_format': '#0.0;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_right_border_number_1digit = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#0.0;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_left_border_number_1digit = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'num_format': '#0.0;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_center_border_number_2digit = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'num_format': '#0.00;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_right_border_number_2digit = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#0.00;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_left_border_number_2digit = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'num_format': '#0.00;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_center_bold_border_number_no_digit = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'num_format': '#;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_center_bold_border_number_1digit = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'num_format': '#0.0;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_right_bold_border_number_1digit = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#0.0;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_left_bold_border_number_1digit = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'num_format': '#0.0;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_center_bold_border_number_2digit = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'num_format': '#0.00;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_left_bold_border_number_2digit = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'num_format': '#0.00;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_right_bold_border_number_2digit = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#0.00;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_right_bold_border = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_right_border = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': False,
        'border': True
    })

    style_11_left_bold_border = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': False,
        'border': True
    })

    style_11_right_border_number_no_digit = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_right_bold_border_number = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#,###',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_right_bold_border_number_no_digit = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_center_border_italic = wb.add_format({
        'bold': False,
        'font_name': 'Times New Roman',
        'italic': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'text_wrap': True,
        'border': True
    })

    style_11_left_border_italic = wb.add_format({
        'bold': False,
        'font_name': 'Times New Roman',
        'italic': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'text_wrap': True,
        'border': True
    })

    style_11_left_italic = wb.add_format({
        'font_size': '11',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'italic': True
    })

    style_11_left_bold_italic = wb.add_format(
        {'bold': True, 'font_size': '11', 'font_color': 'black', 'align': 'left', 'valign': 'vcenter',
         'font_name': 'Times New Roman', 'text_wrap': False, 'italic': True, 'border': False})

    style_11_bold_center = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True
    })

    style_11_bold_center_border_italic = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'italic': True
    })

    style_11_bold_center_border_rotation = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'rotation': 90,
    })

    style_11_bold_right_border_number = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_11_right_border_float = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'num_format': '_(* #,##0_);_(* (#,##0);_(* "-"??_);_(@_)'
    })

    style_11_bold_right_border_float = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'num_format': '_(* #,##0_);_(* (#,##0);_(* "-"??_);_(@_)'
    })

    style_11_bold_right_border_accounting = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'num_format': '#,##0.000'
    })

    style_11_right_border_dot_accounting = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'bottom': 4,
        'top': False,
        'num_format': '#,##0.00'
    })

    style_11_right_border_dot = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'bottom': 4,
        'top': False,
    })

    style_11_center_border_dot = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'bottom': 4,
        'top': False
    })

    style_11_left_border_dot = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'bottom': 4,
        'top': False
    })

    style_11_bold_left_border_dot = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'bottom': 4,
        'top': False,
    })

    style_11_right_format_number = wb.add_format({
        'bold': False,
        'font_size': '11',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'bottom': 4,
        'top': False,
        'num_format': '_(* #,##0_);_(* (#,##0);_(* "-"??_);_(@_)'
    })

    style_11_bold_center_border_dot = wb.add_format({
        'bold': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'bottom': 4,
        'top': False,
    })

    style_12_left_bold_border = wb.add_format({
        'bold': True, 'font_size': '12', 'font_color': 'black', 'align': 'left', 'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_center_border_number_no_digit = wb.add_format({
        'bold': False, 'font_size': '12', 'font_color': 'black', 'align': 'center', 'valign': 'vcenter',
        'num_format': '#,##0.00', 'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_center_bold_border_number_no_digit = wb.add_format({
        'bold': True, 'font_size': '12', 'font_color': 'black', 'align': 'center', 'valign': 'vcenter',
        'num_format': '#,##0.00', 'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_center_bold = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'italic': False, 'border': False,
    })
    style_12_italic_center = wb.add_format({
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'italic': True,
    })

    style_12_italic_right = wb.add_format({
        'font_size': '12',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'italic': True,
    })

    style_12_bold_center_border_1 = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'italic': True, 'border': True,
    })

    style_12_bold_center = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_12_right_format_number = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'num_format': '_(* #,##0_);_(* (#,##0);_(* "-"??_);_(@_)'
    })

    style_12_bold_center_underline = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'underline': True,
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_12_bold_left = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': False,
        'border': False
    })

    style_12_left = wb.add_format({
        'bold': False,
        'font_size': '12',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': False,
        'border': False
    })

    style_12_bold_left_border = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_bold_right_border = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_bold_center_border = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_bold_center_border_89afd7 = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'bg_color': '#89afd7'
    })

    style_12_center_bold_italic = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True, 'italic': True,
        'border': False
    })

    style_12_center_italic = wb.add_format({
        'bold': False,
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True, 'italic': True,
        'border': False
    })

    style_12_center_border = wb.add_format({
        'bold': False,
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_center_border_wrap = wb.add_format({
        'bold': False,
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_center_border_nowrap = wb.add_format({
        'bold': False,
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': False,
        'border': True
    })

    style_12_center_border_italic = wb.add_format({
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'italic': True,
        'border': True
    })

    style_12_bold_right = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': False,
        'border': False
    })

    style_12_bold = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_12_center = wb.add_format({
        'bold': False,
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_12_right_number_no_zero_border = wb.add_format({
        'bold': False,
        'font_size': '12',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'num_format': '0;-0;;@'
    })

    style_12_right_border_number_1digit = wb.add_format({
        'bold': False,
        'font_size': '12',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#0.0;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_right_bold_border_number_1digit = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#0.0;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_right_border_number_2digit = wb.add_format({
        'bold': False,
        'font_size': '12',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#0.00;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_right_bold_border_number_2digit = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#0.00;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })
    style_12_right_border_bold = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_center_border_number = wb.add_format({
        'bold': False,
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'num_format': '#,###'
    })

    style_12_left_border = wb.add_format({
        'bold': False,
        'font_size': '12',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_right_border = wb.add_format({
        'bold': False,
        'font_size': '12',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_right_border_number = wb.add_format({
        'bold': False,
        'font_size': '12',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_right_border_money = wb.add_format({
        'bold': False,
        'font_size': '12',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#,###',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_right_border_money_bold = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#,###',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_center_italic_border = wb.add_format({
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'italic': True,
        'border': True
    })

    style_12_left_italic_bold = wb.add_format({
        'font_size': '12',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'italic': True,
        'bold': True,
    })

    style_12_center_italic_bold = wb.add_format({
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'italic': True,
        'bold': True,
    })

    style_12_left_italic = wb.add_format({
        'font_size': '12',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'italic': True
    })

    style_12_right_bold_border_number = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_left_bold_border_number = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'num_format': '#;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_center_bold_border_money = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'num_format': '#,###',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_center_border_money = wb.add_format({
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'num_format': '#,###',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_right_bold_border_money = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#,###',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_center_bold_border_number = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'num_format': '#;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_center_bold_border_number_2digit = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#0.00;-0;;@',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_12_center_border_1 = wb.add_format({
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'italic': False, 'border': True,
    })

    style_12_center_italic_bold_border = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True, 'italic': True,
        'border': True
    })

    style_12_center_italic_bold_border_color = wb.add_format({
        'bold': True,
        'font_size': '12',
        'font_color': 'black',
        'bg_color': '#a1bfd9',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True, 'italic': True,
        'border': True
    })

    style_13_center = wb.add_format({
        'bold': False,
        'font_size': '13',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_13_left = wb.add_format({
        'bold': False,
        'font_size': '13',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_13_left_border = wb.add_format({
        'bold': False,
        'font_size': '13',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_13_bold_center = wb.add_format({
        'bold': True,
        'font_size': '13',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_13_bold_left = wb.add_format({
        'bold': True,
        'font_size': '13',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_13_bold_center_border = wb.add_format({
        'bold': True,
        'font_size': '13',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_13_bold_center_border_dot = wb.add_format({
        'bold': True,
        'font_size': '13',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'bottom': 4,
        'top': False,
    })

    style_13_bold_left_border_dot = wb.add_format({
        'bold': True,
        'font_size': '13',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'bottom': 4,
        'top': False,
    })

    style_13_center_border_dot = wb.add_format({
        'bold': False,
        'font_size': '13',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'bottom': 4,
        'top': False,
    })

    style_13_left_border_dot = wb.add_format({
        'bold': False,
        'font_size': '13',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'bottom': 4,
        'top': False,
    })

    style_13_right_border_dot = wb.add_format({
        'bold': False,
        'font_size': '13',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'bottom': 4,
        'top': False,
    })

    style_13_right_border_dot_accounting = wb.add_format({
        'bold': False,
        'font_size': '13',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'bottom': 4,
        'top': False,
        'num_format': '#.##'
    })

    style_13_right_border_no_top = wb.add_format({
        'bold': False,
        'font_size': '13',
        'font_color': 'black',
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True,
        'top': False
    })

    style_13_center_italic = wb.add_format({
        'bold': False,
        'font_size': '13',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False,
        'italic': True
    })

    style_13_center_bold_italic = wb.add_format({
        'bold': True,
        'font_size': '13',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False,
        'italic': True
    })

    style_14_center = wb.add_format({
        'font_size': '14',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_14_center_border = wb.add_format({
        'font_size': '14',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_14_left = wb.add_format({
        'font_size': '14',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_14_left_border = wb.add_format({
        'font_size': '14',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_14_bold_center = wb.add_format({
        'bold': True,
        'font_size': '14',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_14_bold_center_border = wb.add_format({
        'bold': True,
        'font_size': '14',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_14_bold_center_italic = wb.add_format({
        'bold': True,
        'font_size': '14',
        'italic': True,
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_14_bold_left = wb.add_format({
        'bold': True,
        'font_size': '14',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_14_bold_left_border = wb.add_format({
        'bold': True,
        'font_size': '14',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_14_center_underline = wb.add_format({
        'font_size': '14',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'underline': True,
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_14_center_border_underline = wb.add_format({
        'font_size': '14',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'underline': True,
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_14_center_italic = wb.add_format({
        'font_size': '14',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'italic': True,
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_14_center_border_italic = wb.add_format({
        'font_size': '14',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'italic': True,
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': True
    })

    style_16_bold_center = wb.add_format({
        'bold': True,
        'font_size': '16',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })
    style_16_bold_left = wb.add_format({
        'bold': True,
        'font_size': '16',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })
    style_24_bold_center = wb.add_format({
        'bold': True,
        'font_size': '24',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_18_bold_center = wb.add_format({
        'bold': True,
        'font_size': '18',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })
    style_18_bold_left = wb.add_format({
        'bold': True,
        'font_size': '18',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_20_bold_center = wb.add_format({
        'bold': True,
        'font_size': '20',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': True,
        'border': False
    })

    style_header_content_noborder_center_italic = wb.add_format({
        'bold': False,
        'font_name': 'Times New Roman',
        'italic': True,
        'font_size': '10',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'text_wrap': True,
        'border': False
    })

    style_hidden = wb.add_format({
        'hidden': True,
        'font_size': '11',
        'font_color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Times New Roman',
        'text_wrap': False,
        'border': False
    })

    style_header_table = wb.add_format({
        'pattern': True, 'bg_color': '#95B3D7', 'font_name': 'Times New Roman',
        'font_color': 'black', 'align': 'center', 'font_size': '11',
        'valign': 'vcenter', 'text_wrap': True, 'bold': True,
        'border': True
    })

    style_number_2digit = wb.add_format({
        'bold': True,
        'font_name': 'Times New Roman',
        'num_format': '#,##0.00',
        'font_size': '10',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'text_wrap': True,
        'border': True
    })
    style_number_3digit = wb.add_format({
        'bold': True,
        'font_name': 'Times New Roman',
        'num_format': '#,##0.000',
        'font_size': '10',
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'text_wrap': True,
        'border': True
    })
    return {
        'style_7_right_border': style_7_right_border,
        'style_7_bold_right': style_7_bold_right,
        'style_7_bold_left': style_7_bold_left,
        'style_7_bold_center': style_7_bold_center,
        'style_7_left': style_7_left,
        'style_7_left_border': style_7_left_border,
        'style_7_center': style_7_center,
        'style_7_center_italic': style_7_center_italic,
        'style_7_center_border': style_7_center_border,
        'style_7_bold_center_border': style_7_bold_center_border,
        'style_8_center': style_8_center,
        'style_8_center_italic': style_8_center_italic,
        'style_8_center_italic_bold': style_8_center_italic_bold,
        'style_8_center_italic_bold_border': style_8_center_italic_bold_border,
        'style_8_center_italic_bold_border_color': style_8_center_italic_bold_border_color,
        'style_8_center_border': style_8_center_border,
        'style_8_left': style_8_left,
        'style_8_left_no_text_wrap': style_8_left_no_text_wrap,
        'style_8_left_number': style_8_left_number,
        'style_8_right_number': style_8_right_number,
        'style_8_right_number_border': style_8_right_number_border,
        'style_8_left_border': style_8_left_border,
        'style_8_right_border': style_8_right_border,
        'style_8_bold_center_border': style_8_bold_center_border,
        'style_8_bold_left': style_8_bold_left,
        'style_8_bold_right': style_8_bold_right,
        'style_8_bold_center': style_8_bold_center,
        'style_8_bold_left_border': style_8_bold_left_border,
        'style_8_bold_right_border': style_8_bold_right_border,
        'style_8_bold_right_border_number': style_8_bold_right_border_number,
        'style_8_left_bold_no_border': style_8_left_bold_no_border,
        'style_9_bold_center_border': style_9_bold_center_border,
        'style_9_bold_right_border': style_9_bold_right_border,
        'style_9_bold_left_border': style_9_bold_left_border,
        'style_9_bold_center_border_rotation': style_9_bold_center_border_rotation,
        'style_9_right_border': style_9_right_border,
        'style_9_left_border': style_9_left_border,
        'style_9_center_border': style_9_center_border,
        'style_9_center_border_italic': style_9_center_border_italic,
        'style_9_bold_left_top_border_diag': style_9_bold_left_top_border_diag,
        'style_9_bold_center_border_italic': style_9_bold_center_border_italic,
        'style_9_bold_right_border_italic': style_9_bold_right_border_italic,
        'style_9_left_border_italic': style_9_left_border_italic,
        'style_9_left': style_9_left,
        'style_9_bold_left': style_9_bold_left,
        'style_9_bold_center': style_9_bold_center,
        'style_9_center_border_rotation': style_9_center_border_rotation,
        'style_9_bold_left_border_red': style_9_bold_left_border_red,
        'style_9_right_border_italic': style_9_right_border_italic,
        'style_9_bold_center_wrap_border': style_9_bold_center_wrap_border,
        'style_9_center_wrap_border': style_9_center_wrap_border,
        'style_9_left_wrap_border': style_9_left_wrap_border,
        'style_9_left_italic': style_9_left_italic,
        'style_9_center_border_top_italic': style_9_center_border_top_italic,
        'style_9_center_border_bottom_italic': style_9_center_border_bottom_italic,
        'style_9_center_border_continuous': style_9_center_border_continuous,
        'style_9_left_border_continuous': style_9_left_border_continuous,
        'style_9_right_border_continuous': style_9_right_border_continuous,
        'style_9_bold_center_border_continuous': style_9_bold_center_border_continuous,
        'style_9_bold_left_border_continuous': style_9_bold_left_border_continuous,
        'style_9_bold_right_border_continuous': style_9_bold_right_border_continuous,
        'style_10_right': style_10_right,
        'style_10_center': style_10_center,
        'style_10_bold_left': style_10_bold_left,
        'style_10_bold_right': style_10_bold_right,
        'style_10_bold_center_border': style_10_bold_center_border,
        'style_10_bold_right_border': style_10_bold_right_border,
        'style_10_bold_left_border': style_10_bold_left_border,
        'style_10_bold_left_border_bottom': style_10_bold_left_border_bottom,
        'style_10_bold_center_border_rotation': style_10_bold_center_border_rotation,
        'style_10_center_border_rotation_red': style_10_center_border_rotation_red,
        'style_10_right_border': style_10_right_border,
        'style_10_left_border': style_10_left_border,
        'style_10_left_border_bottom': style_10_left_border_bottom,
        'style_10_center_border': style_10_center_border,
        'style_10_center_border_red': style_10_center_border_red,
        'style_10_left_border_red': style_10_left_border_red,
        'style_10_center_italic': style_10_center_italic,
        'style_10_center_italic_border': style_10_center_italic_border,
        'style_10_left_italic': style_10_left_italic,
        'style_10_left_italic_border': style_10_left_italic_border,
        'style_10_right_italic': style_10_right_italic,
        'style_10_bold_left_italic': style_10_bold_left_italic,
        'style_10_center_border_italic': style_10_center_border_italic,
        'style_10_bold_left_top_border_diag': style_10_bold_left_top_border_diag,
        'style_10_bold_center_border_italic': style_10_bold_center_border_italic,
        'style_10_bold_right_border_italic': style_10_bold_right_border_italic,
        'style_10_left_border_italic': style_10_left_border_italic,
        'style_10_left': style_10_left,
        'style_10_left_red': style_10_left_red,
        'style_10_bold_center': style_10_bold_center,
        'style_10_center_border_rotation': style_10_center_border_rotation,
        'style_10_bold_left_border_red': style_10_bold_left_border_red,
        'style_10_bold_center_border_red': style_10_bold_center_border_red,
        'style_10_right_bold_border_money': style_10_right_bold_border_money,
        'style_10_right_bold_border_number': style_10_right_bold_border_number,
        'style_10_right_italic_border_number': style_10_right_italic_border_number,
        'style_10_right_border_money': style_10_right_border_money,
        'style_10_right_italic_border_money': style_10_right_italic_border_money,
        'style_10_right_border_number': style_10_right_border_number,
        'style_11_left': style_11_left,
        'style_11_center': style_11_center,
        'style_11_center_border': style_11_center_border,
        'style_11_left_border': style_11_left_border,
        'style_11_right_border_number': style_11_right_border_number,
        'style_11_bold_center_border': style_11_bold_center_border,
        'style_11_bold_left': style_11_bold_left,
        'style_11_bold_left_border': style_11_bold_left_border,
        'style_11_bold_right_border': style_11_bold_right_border,
        'style_11_bold_center_underline': style_11_bold_center_underline,
        'style_11_left_bold': style_11_left_bold,
        'style_11_center_bold': style_11_center_bold,
        'style_11_center_italic': style_11_center_italic,
        'style_11_center_italic_bold': style_11_center_italic_bold,
        'style_11_left_border_right': style_11_left_border_right,
        'style_11_left_bold_border': style_11_left_bold_border,
        'style_11_right_border': style_11_right_border,
        'style_11_bold_right': style_11_bold_right,
        'style_11_right_bold_border': style_11_right_bold_border,
        'style_11_left_wrap_border': style_11_left_wrap_border,
        'style_11_left_bold_number': style_11_left_bold_number,
        'style_11_left_bold_no_border': style_11_left_bold_no_border,
        'style_11_bold_left_wrap_border': style_11_bold_left_wrap_border,
        'style_11_bold_center_wrap_border': style_11_bold_center_wrap_border,
        'style_11_center_wrap_border': style_11_center_wrap_border,
        'style_11_middle_wrap_border': style_11_middle_wrap_border,
        'style_11_center_bold_border': style_11_center_bold_border,
        'style_11_center_border_number': style_11_center_border_number,
        'style_11_center_bold_border_number': style_11_center_bold_border_number,
        'style_11_center_border_number_no_digit': style_11_center_border_number_no_digit,
        'style_11_center_border_number_1digit': style_11_center_border_number_1digit,
        'style_11_right_border_number_1digit': style_11_right_border_number_1digit,
        'style_11_left_border_number_1digit': style_11_left_border_number_1digit,
        'style_11_center_border_number_2digit': style_11_center_border_number_2digit,
        'style_11_right_border_number_2digit': style_11_right_border_number_2digit,
        'style_11_left_border_number_2digit': style_11_left_border_number_2digit,
        'style_11_center_bold_border_number_no_digit': style_11_center_bold_border_number_no_digit,
        'style_11_center_bold_border_number_1digit': style_11_center_bold_border_number_1digit,
        'style_11_left_bold_border_number_1digit': style_11_left_bold_border_number_1digit,
        'style_11_right_bold_border_number_1digit': style_11_right_bold_border_number_1digit,
        'style_11_center_bold_border_number_2digit': style_11_center_bold_border_number_2digit,
        'style_11_left_bold_border_number_2digit': style_11_left_bold_border_number_2digit,
        'style_11_right_bold_border_number_2digit': style_11_right_bold_border_number_2digit,
        'style_11_right_border_number_no_digit': style_11_right_border_number_no_digit,
        'style_11_right_bold_border_number': style_11_right_bold_border_number,
        'style_11_right_bold_border_number_no_digit': style_11_right_bold_border_number_no_digit,
        'style_11_center_border_italic': style_11_center_border_italic,
        'style_11_left_border_italic': style_11_left_border_italic,
        'style_11_left_italic': style_11_left_italic,
        'style_11_left_bold_italic': style_11_left_bold_italic,
        'style_11_bold_center': style_11_bold_center,
        'style_11_bold_center_border_italic': style_11_bold_center_border_italic,
        'style_11_bold_center_border_rotation': style_11_bold_center_border_rotation,
        'style_11_center_border_dot': style_11_center_border_dot,
        'style_11_left_border_dot': style_11_left_border_dot,
        'style_11_bold_right_border_number': style_11_bold_right_border_number,
        'style_11_right_border_float': style_11_right_border_float,
        'style_11_bold_right_border_float': style_11_bold_right_border_float,
        'style_11_bold_right_border_accounting': style_11_bold_right_border_accounting,
        'style_11_right_border_dot_accounting': style_11_right_border_dot_accounting,
        'style_11_right_border_dot': style_11_right_border_dot,
        'style_11_bold_left_border_dot': style_11_bold_left_border_dot,
        'style_11_right_format_number': style_11_right_format_number,
        'style_11_bold_center_border_dot': style_11_bold_center_border_dot,
        'style_12_right_format_number': style_12_right_format_number,
        'style_12_bold_center_underline': style_12_bold_center_underline,
        'style_12_bold_left_border': style_12_bold_left_border,
        'style_12_bold_right_border': style_12_bold_right_border,
        'style_12_bold_center_border': style_12_bold_center_border,
        'style_12_bold_center_border_89afd7': style_12_bold_center_border_89afd7,
        'style_12_italic_center_wrap': style_12_italic_center_wrap,
        'style_12_italic_left_wrap': style_12_italic_left_wrap,
        'style_12_left': style_12_left,
        'style_12_center_bold_italic': style_12_center_bold_italic,
        'style_12_center_italic': style_12_center_italic,
        'style_12_center_border': style_12_center_border,
        'style_12_center_border_wrap': style_12_center_border_wrap,
        'style_12_center_border_nowrap': style_12_center_border_nowrap,
        'style_12_center_border_italic': style_12_center_border_italic,
        'style_12_bold_right': style_12_bold_right,
        'style_12_bold': style_12_bold,
        'style_12_center': style_12_center,
        'style_12_right_number_no_zero_border': style_12_right_number_no_zero_border,
        'style_12_right_border_number_1digit': style_12_right_border_number_1digit,
        'style_12_right_border_number_2digit': style_12_right_border_number_2digit,
        'style_12_right_bold_border_number_1digit': style_12_right_bold_border_number_1digit,
        'style_12_right_bold_border_number_2digit': style_12_right_bold_border_number_2digit,
        'style_12_center_border_number': style_12_center_border_number,
        'style_12_left_border': style_12_left_border,
        'style_12_right_border': style_12_right_border,
        'style_12_right_border_number': style_12_right_border_number,
        'style_12_right_border_money': style_12_right_border_money,
        'style_12_right_border_money_bold': style_12_right_border_money_bold,
        'style_12_center_italic_border': style_12_center_italic_border,
        'style_12_left_italic': style_12_left_italic,
        'style_12_left_italic_bold': style_12_left_italic_bold,
        'style_12_center_italic_bold': style_12_center_italic_bold,
        'style_12_right_bold_border_number': style_12_right_bold_border_number,
        'style_12_left_bold_border_number': style_12_left_bold_border_number,
        'style_12_center_bold_border_money': style_12_center_bold_border_money,
        'style_12_center_border_money': style_12_center_border_money,
        'style_12_right_bold_border_money': style_12_right_bold_border_money,
        'style_12_center_bold_border_number': style_12_center_bold_border_number,
        'style_12_center_bold_border_number_2digit': style_12_center_bold_border_number_2digit,
        'style_12_center_border_1': style_12_center_border_1,
        'style_12_center_italic_bold_border': style_12_center_italic_bold_border,
        'style_12_center_italic_bold_border_color': style_12_center_italic_bold_border_color,
        'style_12_bold_center_border_rotation': style_12_bold_center_border_rotation,

        'style_12_bold_center': style_12_bold_center,
        'style_12_bold_left': style_12_bold_left,
        'style_12_center_border_number_no_digit': style_12_center_border_number_no_digit,
        'style_12_center_bold_border_number_no_digit': style_12_center_bold_border_number_no_digit,
        'style_12_left_bold_border': style_12_left_bold_border,
        'style_12_center_bold': style_12_center_bold,
        'style_12_italic_center': style_12_italic_center,
        'style_12_italic_right': style_12_italic_right,
        'style_12_bold_center_border_1': style_12_bold_center_border_1,

        'style_13_center': style_13_center,
        'style_13_left': style_13_left,
        'style_13_left_border': style_13_left_border,
        'style_13_bold_center': style_13_bold_center,
        'style_13_bold_left': style_13_bold_left,
        'style_13_bold_center_border': style_13_bold_center_border,
        'style_13_bold_center_border_dot': style_13_bold_center_border_dot,
        'style_13_bold_left_border_dot': style_13_bold_left_border_dot,
        'style_13_center_border_dot': style_13_center_border_dot,
        'style_13_left_border_dot': style_13_left_border_dot,
        'style_13_right_border_dot': style_13_right_border_dot,
        'style_13_center_italic': style_13_center_italic,
        'style_13_center_bold_italic': style_13_center_bold_italic,
        'style_13_right_border_dot_accounting': style_13_right_border_dot_accounting,
        'style_13_right_border_no_top': style_13_right_border_no_top,
        'style_14_center': style_14_center,
        'style_14_left': style_14_left,
        'style_14_bold_center': style_14_bold_center,
        'style_14_bold_center_italic': style_14_bold_center_italic,
        'style_14_center_underline': style_14_center_underline,
        'style_14_center_italic': style_14_center_italic,
        'style_14_bold_left': style_14_bold_left,
        'style_14_center_border': style_14_center_border,
        'style_14_left_border': style_14_left_border,
        'style_14_bold_center_border': style_14_bold_center_border,
        'style_14_center_border_underline': style_14_center_border_underline,
        'style_14_center_border_italic': style_14_center_border_italic,
        'style_14_bold_left_border': style_14_bold_left_border,
        'style_16_bold_center': style_16_bold_center,
        'style_16_bold_left': style_16_bold_left,
        'style_18_bold_center': style_18_bold_center,
        'style_18_bold_left': style_18_bold_left,
        'style_20_bold_center': style_20_bold_center,
        'style_24_bold_center': style_24_bold_center,
        'style_header_content_noborder_center_italic': style_header_content_noborder_center_italic,
        'style_hidden': style_hidden,
        'style_header_table': style_header_table,
        'style_12_center_border_rotation': style_12_center_border_rotation,
        'style_12_right_border_bold': style_12_right_border_bold,
        'style_11_center_italic_border': style_11_center_italic_border,
        'style_number_2digit': style_number_2digit,
        'style_number_3digit': style_number_3digit,
    }
