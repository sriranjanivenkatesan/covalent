/**
 * Copyright 2021 Agnostiq Inc.
 *
 * This file is part of Covalent.
 *
 * Licensed under the GNU Affero General Public License 3.0 (the "License").
 * A copy of the License may be obtained with this software package or at
 *
 *      https://www.gnu.org/licenses/agpl-3.0.en.html
 *
 * Use of this file is prohibited except in compliance with the License. Any
 * modifications or derivative works of this file must retain this copyright
 * notice, and modified files must contain a notice indicating that they have
 * been altered from the originals.
 *
 * Covalent is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE. See the License for more details.
 *
 * Relief from the License may be granted by purchasing a commercial license.
 */

import React, { useEffect, useState } from 'react'
import {
  Container,
  Grid,
  Box,
  Input,
  InputLabel,
  Radio,
  RadioGroup,
  Button,
  Stack,
  Snackbar,
  SvgIcon,
  InputAdornment,
  IconButton,
  Select,
  MenuItem,
} from '@mui/material'
import { Clear as ClearIcon, Search as SearchIcon } from '@mui/icons-material'
import Typography from '@mui/material/Typography'
import List from '@mui/material/List'
import ListItem from '@mui/material/ListItem'
import ListItemButton from '@mui/material/ListItemButton'
import ListItemText from '@mui/material/ListItemText'
import ListItemIcon from '@mui/material/ListItemIcon'
import Collapse from '@mui/material/Collapse'
import ExpandMore from '@mui/icons-material/ExpandMore'
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight'
import FormControlLabel from '@mui/material/FormControlLabel'
import FormControl from '@mui/material/FormControl'
import FormLabel from '@mui/material/FormLabel'
import { settingsResults, updateSettings } from '../../redux/settingsSlice'
import { useDispatch, useSelector } from 'react-redux'
import _, { capitalize } from 'lodash'
import Skeleton from '@mui/material/Skeleton'
import { ReactComponent as closeIcon } from '../../assets/close.svg'
import { toggleLatticeDrawer } from '../../redux/popupSlice'
import { styled } from '@mui/material/styles'

const SettingsCard = () => {
  const dispatch = useDispatch()
  const serverName = 'server'
  const accName = 'client'
  const [open, setOpen] = useState(false)
  const [subMenu, setSubMenu] = useState([])
  const [resultKey, setResultKey] = useState('sdk')
  const [resultOutput, setResultOutput] = useState()
  const settings_result = useSelector(
    (state) => state.settingsResults.settingsList
  )
  const menuCallResult = useSelector((state) => state.dataRes.popupData)
  const [openSnackbar, setOpenSnackbar] = useState(false)
  const [snackbarMessage, setSnackbarMessage] = useState(null)
  const [isDisabled, setIsDisabled] = useState(false)
  const [handle, setHandle] = useState('')
  const [searchData, setSearchData] = useState(settings_result)
  const [searchKey, setSearchKey] = useState('')
  const [restoreData, setRestoreData] = useState()
  const [valueChange, setValueChange] = useState(false)
  const [clientDetail, setClientDetail] = useState(null)
  const [serverDetail, setServerDetail] = useState(null)
  const [tempData, setTempData] = useState(null)
  const [tempDataServer, setTempDataServer] = useState(null)

  useEffect(() => {
    dispatch(settingsResults())
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    if (valueChange) {
      const settingObj = {
        isChanged: valueChange,
        data: resultOutput,
        nodeName: resultKey,
        mainKey: accName
      }
      dispatch(toggleLatticeDrawer(settingObj))
    } else {
      const settingObj = {
        isChanged: valueChange,
      }
      dispatch(toggleLatticeDrawer(settingObj))
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [valueChange, resultOutput])

  useEffect(() => {
    if (settings_result) {
      setSearchData(Object.values(settings_result)[0])
      setClientDetail(Object.values(settings_result)[0])
      setServerDetail(Object.values(settings_result)[1])
      setTempData(Object.values(settings_result)[0])
      setTempDataServer(Object.values(settings_result)[1])
    }
  }, [settings_result])

  useEffect(() => {
    if (_.size(searchData) !== 0) {
      setResultOutput(Object.values(searchData)[0])
      setRestoreData(Object.values(searchData)[0])
    }
  }, [searchData])

  const handleSubmit = (event) => {
    event.preventDefault()
    const updateData = {
      [accName]: {
        [resultKey]: resultOutput,
      },
    }
    dispatch(updateSettings(updateData)).then((action) => {
      if (action.type === updateSettings.fulfilled.type) {
        setOpenSnackbar(true)
        setSnackbarMessage('Settings Updated Successfully')
        setValueChange(false)
        setClientDetail((currValue) => ({
          ...currValue,
          [resultKey]: resultOutput,
        }))
        setRestoreData(resultOutput)
      } else if (action.type === updateSettings.rejected.type) {
        setOpenSnackbar(true)
        setSnackbarMessage(
          'Something went wrong and could not settings updated!'
        )
      }
    })
    setHandle('')
  }

  const getSubmenuName = (name) => {
    let formattedName = name
    const uSpliit = name.includes('_')
    if (uSpliit) {
      var a = name
        .replace(name.at(0), name.at(0).toLocaleUpperCase())
        .substring(0, name.indexOf('_'))
      var b = name
        .replace(name.at(0), name.at(0).toLocaleUpperCase())
        .substring(name.indexOf('_') + 1, name.length)
      formattedName = a + ' ' + b.replace(b.at(0), b.at(0).toLocaleUpperCase())
    } else {
      if (name === 'slurm') {
        formattedName = name.toUpperCase()
      } else if (name === 'dask') {
        formattedName = name.toUpperCase()
      } else {
        formattedName = name.charAt(0).toUpperCase() + name.slice(1)
      }
    }
    return formattedName
  }

  const getLabelName = (name) => {
    let formattedName = name
    const uSpliit = name.includes('_')
    if (uSpliit) {
      var a = name
        .replace(name.at(0), name.at(0).toLocaleUpperCase())
        .substring(0, name.indexOf('_'))
      var b = name
        .replace(name.at(0), name.at(0).toLocaleUpperCase())
        .substring(name.indexOf('_') + 1, name.length)
      formattedName = a + ' ' + b.replace(b.at(0), b.at(0))
    } else {
      if (name === 'sdk') {
        formattedName = name.toUpperCase()
      } else {
        formattedName = name.charAt(0).toUpperCase() + name.slice(1)
      }
    }
    if (formattedName === 'Cache dir') {
      formattedName = 'Cache directory'
    } else if (formattedName === 'Results dir') {
      formattedName = 'Results directory'
    } else if (formattedName === 'Executor dir') {
      formattedName = 'Executor directory'
    } else if (formattedName === 'Log stdout') {
      formattedName = 'Log standard out'
    } else if (formattedName === 'Log dir') {
      formattedName = 'Log directory'
    } else if (formattedName === 'Base dir') {
      formattedName = 'Base directory'
    }
    return formattedName
  }

  const getSettingsName = (name) => {
    let formattedName = name
    const uSpliit = name.includes('_')
    if (uSpliit) {
      var a = name
        .replace(name.at(0), name.at(0).toLocaleUpperCase())
        .substring(0, name.indexOf('_'))
      var b = name
        .replace(name.at(0), name.at(0).toLocaleUpperCase())
        .substring(name.indexOf('_') + 1, name.length)
      formattedName = a + ' ' + b.replace(b.at(0), b.at(0).toLocaleUpperCase())
    } else {
      if (name === 'sdk' || name === 'dask') {
        formattedName = name.toUpperCase()
      } else {
        formattedName = name.charAt(0).toUpperCase() + name.slice(1)
      }
    }
    return formattedName
  }

  const isChildHasList = (item) => {
    let childIsObject = false
    _.map(item, function (value) {
      if (_.isObject(value)) childIsObject = true
    })
    return childIsObject
  }

  const handleClick = (item) => {
    _.map(item, function (value, key) {
      if (_.isObject(value)) {
        setOpen(!open)
        setSubMenu(item)
      } else {
        setOpen(false)
      }
    })
  }

  const menuClick = (value, key, panel) => {
    if (panel === 'client') {
      setIsDisabled(false)
    } else {
      setIsDisabled(true)
    }
    setRestoreData(value)
    if (menuCallResult.isChanged) {
      const updateData = {
        [accName]: {
          [resultKey]: resultOutput,
        },
      }
      dispatch(updateSettings(updateData)).then((action) => {
        if (action.type === updateSettings.fulfilled.type) {
          setOpenSnackbar(true)
          setSnackbarMessage('Settings Updated Successfully')
          setValueChange(false)
          setClientDetail((currValue) => ({
            ...currValue,
            [resultKey]: resultOutput,
          }))
          setRestoreData(resultOutput)
        } else if (action.type === updateSettings.rejected.type) {
          setOpenSnackbar(true)
          setSnackbarMessage(
            'Something went wrong and could not settings updated!'
          )
        }
      })
      setHandle('')
      setIsDisabled(false)
    } else {
      setValueChange(false)
      setResultKey(key)
      setResultOutput(value)
    }
  }

  const handleKeypress = (event) => {
    setHandle(event.key)
    setValueChange(true)
  }

  const onInputExecutorChange = (e, subkey, key) => {
    setResultOutput((currValue) => ({
      ...currValue,
      [key]: {
        ...currValue[key],
        [subkey]: e.target.value,
      },
    }))
  }

  const handleChange = (e, key) => {
    setHandle(e.target.value)
    setValueChange(true)
    setResultOutput((currValue) => ({
      ...currValue,
      [key]: e.target.value,
    }))
  }

  const handleSelectChange = (e, key) => {
    setHandle(e.target.value)
    setValueChange(true)
    setResultOutput((currValue) => ({
      ...currValue,
      [key]: e.target.value,
    }))
  }

  const cancelButton = () => {
    if (handle) {
      setResultOutput(restoreData)
      setHandle('')
      setValueChange(false)
    }
  }

  const handleInputChange = (e) => {
    setSearchKey(e.target.value)
    const filterData = Object.fromEntries(
      Object.entries(tempData).filter(([key]) =>
        key.includes(e.target.value.toLowerCase())
      )
    )
    const filterData1 = Object.fromEntries(
      Object.entries(tempDataServer).filter(([key]) =>
        key.includes(e.target.value.toLowerCase())
      )
    )
    setClientDetail(filterData)
    setServerDetail(filterData1)
  }

  const handleSearchClear = () => {
    setSearchKey('')
    setClientDetail(Object.values(settings_result)[0])
    setServerDetail(Object.values(settings_result)[1])
  }

  const handleSubmenuClick = (value, key) => {
    if (resultKey !== 'executors') {
      setValueChange(false)
      setResultKey('executors')
      setResultOutput(value)
    } else {
      document.getElementById(key).scrollIntoView({ behavior: 'smooth' })
    }
  }

  const onInputChange = (e, key) => {
    setResultOutput((currValue) => ({
      ...currValue,
      [key]: e.target.value,
    }))
  }

  const StyledList = styled(List)({
    // hover states
    '& .MuiListItemButton-root:hover': {
      backgroundColor: '#1C1C46',
      borderRadius: '8px',
      '&, & .MuiListItemIcon-root': {
        color: 'white',
      },
    },
  })

  return (
    <Container maxWidth="xl" sx={{ mb: 4, marginTop: '32px' }}>
      <Snackbar
        open={openSnackbar}
        autoHideDuration={3000}
        message={snackbarMessage}
        onClose={() => setOpenSnackbar(false)}
        action={
          <SvgIcon
            sx={{
              mt: 2,
              zIndex: 2,
              cursor: 'pointer',
            }}
            component={closeIcon}
            onClick={() => setOpenSnackbar(false)}
          />
        }
      />
      <Typography
        component="h4"
        sx={{
          mb: 5,
          color: (theme) => theme.palette.primary.white,
          fontSize: '32px',
        }}
      >
        Settings
      </Typography>
      {_.size(settings_result) !== 0 ? (
        <Box>
          <Grid container spacing={3}>
            <Grid
              item
              xs={3}
              sx={(theme) => ({
                borderRight: 1,
                borderColor: theme.palette.background.coveBlack02,
              })}
            >
              <Box>
                <Input
                  sx={{
                    px: 2,
                    py: 0.5,
                    width: '278px',
                    height: '32px',
                    border: '1px solid #303067',
                    borderRadius: '60px',
                    mb: 3,
                  }}
                  disableUnderline
                  value={searchKey}
                  autoComplete="off"
                  startAdornment={
                    <InputAdornment position="start">
                      <SearchIcon
                        sx={{ color: 'text.secondary', fontSize: 18 }}
                      />
                    </InputAdornment>
                  }
                  endAdornment={
                    <InputAdornment
                      position="end"
                      sx={{
                        visibility: searchKey !== '' ? 'visible' : 'hidden',
                      }}
                    >
                      <IconButton
                        size="small"
                        onClick={() => handleSearchClear()}
                      >
                        <ClearIcon
                          fontSize="inherit"
                          sx={{ color: 'text.secondary' }}
                        />
                      </IconButton>
                    </InputAdornment>
                  }
                  onChange={(e) => handleInputChange(e)}
                  placeholder="Search"
                />
                <Typography
                  variant="h6"
                  component="h6"
                  sx={(theme) => ({
                    color: theme.palette.primary.white,
                    fontWeight: 'bold',
                    mb: 2,
                  })}
                >
                  {capitalize(accName)}
                </Typography>
                {_.map(clientDetail, function (menuValue, menuKey) {
                  return (
                    <StyledList sx={{ pb: 0, pt: 0 }} key={menuKey}>
                      <ListItem disablePadding>
                        <ListItemButton
                          onClick={
                            isChildHasList
                              ? () => handleClick(menuValue)
                              : () => { }
                          }
                          sx={{
                            right: isChildHasList(menuValue) ? '0px' : '0px',
                          }}
                        >
                          {isChildHasList(menuValue) && (
                            <ListItemIcon>
                              {open ? (
                                <ExpandMore />
                              ) : (
                                <KeyboardArrowRightIcon />
                              )}
                            </ListItemIcon>
                          )}
                          <ListItemText
                            inset
                            primary={getSettingsName(menuKey)}
                            onClick={() =>
                              menuClick(menuValue, menuKey, accName)
                            }
                            disableTypography
                            sx={{
                              color:
                                resultKey === menuKey
                                  ? 'white'
                                  : 'text.primary',
                              pl: '0px',
                              fontSize: '14px',
                              fontWeight:
                                resultKey === menuKey ? 'bold' : 'normal',
                            }}
                          />
                        </ListItemButton>
                      </ListItem>
                    </StyledList>
                  )
                })}

                {open && (
                  <Collapse in={open} timeout="auto" unmountOnExit>
                    <List component="div" disablePadding>
                      {_.map(subMenu, function (value, key) {
                        return (
                          <StyledList sx={{ pb: 0, pt: 0 }} key={key}>
                            <ListItem disablePadding>
                              <ListItemButton sx={{ pl: 9, pt: 0.3, pb: 0.3 }}>
                                <ListItemText
                                  inset
                                  primary={getSubmenuName(key)}
                                  onClick={() =>
                                    handleSubmenuClick(subMenu, key)
                                  }
                                  disableTypography
                                  sx={{ pl: '0px', fontSize: '14px' }}
                                />
                              </ListItemButton>
                            </ListItem>
                          </StyledList>
                        )
                      })}
                    </List>
                  </Collapse>
                )}
              </Box>

              <Box>
                <Typography
                  variant="h6"
                  component="h6"
                  sx={(theme) => ({
                    color: theme.palette.primary.white,
                    fontWeight: 'bold',
                    mb: 2,
                    mt: 2,
                  })}
                >
                  {capitalize(serverName)}
                </Typography>
                {_.map(serverDetail, function (menuValue, menuKey) {
                  return (
                    <StyledList sx={{ pb: 0, pt: 0 }} key={menuKey}>
                      <ListItem disablePadding>
                        <ListItemButton
                          onClick={
                            isChildHasList
                              ? () => handleClick(menuValue)
                              : () => { }
                          }
                          sx={{
                            right: isChildHasList(menuValue) ? '0px' : '0px',
                          }}
                        >
                          {isChildHasList(menuValue) && (
                            <ListItemIcon>
                              {open ? (
                                <ExpandMore />
                              ) : (
                                <KeyboardArrowRightIcon />
                              )}
                            </ListItemIcon>
                          )}
                          <ListItemText
                            inset
                            primary={getSettingsName(menuKey)}
                            onClick={() => menuClick(menuValue, menuKey)}
                            disableTypography
                            sx={{
                              color:
                                resultKey === menuKey
                                  ? 'white'
                                  : 'text.primary',
                              pl: '0px',
                              fontSize: '14px',
                              fontWeight:
                                resultKey === menuKey ? 'bold' : 'normal',
                            }}
                          />
                        </ListItemButton>
                      </ListItem>
                    </StyledList>
                  )
                })}
              </Box>
            </Grid>
            <Grid item xs={9}>
              <Typography
                component="h6"
                sx={{
                  fontWeight: 'bold',
                  fontSize: '24px',
                  color: (theme) => theme.palette.primary.white,
                }}
              >
                {getSettingsName(resultKey)}
              </Typography>
              <Grid container spacing={3} sx={{ mt: 2 }}>
                <Grid item xs={7}>
                  <form onSubmit={handleSubmit} id="get__pop_id">
                    {_.map(resultOutput, function (value, key) {
                      return (
                        <Box sx={{ mb: 3 }} key={key}>
                          {_.isObject(value) ? (
                            <Box key={key} id={key}>
                              <Typography
                                variant="h6"
                                component="h6"
                                sx={(theme) => ({
                                  color: theme.palette.primary.light,
                                  fontWeight: 'bold',
                                })}
                              >
                                {getSettingsName(key)}
                              </Typography>
                              {_.map(value, function (item, key1) {
                                return (
                                  <Box sx={{ mt: 3 }} key={key1}>
                                    {value === 'true' || value === 'false' ? (
                                      <FormControl>
                                        <FormLabel
                                          id="demo-row-radio-buttons-group-label"
                                          sx={(theme) => ({
                                            fontSize: '14px',
                                            color: 'text.primary',
                                          })}
                                        >
                                          {' '}
                                          {getSettingsName(key1)}
                                        </FormLabel>
                                        <RadioGroup
                                          row
                                          onChange={handleChange}
                                          aria-labelledby="demo-row-radio-buttons-group-label"
                                          name="row-radio-buttons-group"
                                        >
                                          <FormControlLabel
                                            value="true"
                                            disabled={isDisabled}
                                            control={<Radio />}
                                            label={
                                              <Typography
                                                sx={{ fontSize: '14px' }}
                                              >
                                                True
                                              </Typography>
                                            }
                                          />
                                          <FormControlLabel
                                            value="false"
                                            disabled={isDisabled}
                                            control={<Radio />}
                                            label={
                                              <Typography
                                                sx={{
                                                  fontSize: '14px',
                                                }}
                                              >
                                                False
                                              </Typography>
                                            }
                                          />
                                        </RadioGroup>
                                      </FormControl>
                                    ) : (
                                      <>
                                        <InputLabel
                                          variant="standard"
                                          htmlFor="uncontrolled-native"
                                          sx={{
                                            fontSize: '14px',
                                            mb: 1,
                                            color: 'text.primary',
                                          }}
                                        >
                                          {getLabelName(key1)}
                                        </InputLabel>
                                        <Input
                                          sx={{
                                            px: 2,
                                            py: 0.5,
                                            width: '360px',
                                            height: '32px',
                                            border: '1px solid #303067',
                                            borderRadius: '60px',
                                            fontSize: '14px',
                                            color: (theme) =>
                                              theme.palette.text.secondary,
                                          }}
                                          disabled={isDisabled}
                                          onKeyDown={handleKeypress}
                                          autoComplete="off"
                                          name={key1}
                                          onChange={(e) =>
                                            onInputExecutorChange(e, key1, key)
                                          }
                                          value={item}
                                          disableUnderline
                                          placeholder={key1}
                                        />
                                      </>
                                    )}
                                  </Box>
                                )
                              })}
                            </Box>
                          ) : (
                            <>
                              {key === 'log_level' ? (
                                <Box
                                  sx={{
                                    display: 'flex',
                                    flexDirection: 'column',
                                    alignContent: 'flex-start',
                                  }}
                                >
                                  <FormLabel
                                    id="demo-simple-select-label"
                                    sx={{
                                      fontSize: '14px',
                                      color: 'text.primary',
                                    }}
                                  >
                                    {' '}
                                    {getSettingsName(key)}
                                  </FormLabel>

                                  <Select
                                    labelId="demo-simple-select-label"
                                    id="demo-simple-select"
                                    value={value}
                                    name={key}
                                    label={key}
                                    onChange={(e) => handleSelectChange(e, key)}
                                    sx={{
                                      mt: 1,
                                      fontSize: '14px',
                                      width: '140px',
                                      height: '32px',
                                    }}
                                    className="dropdownSelect"
                                  >
                                    <MenuItem
                                      sx={{ fontSize: '14px' }}
                                      value="notset"
                                    >
                                      Notset
                                    </MenuItem>
                                    <MenuItem
                                      sx={{ fontSize: '14px' }}
                                      value="debug"
                                    >
                                      Debug
                                    </MenuItem>
                                    <MenuItem
                                      sx={{ fontSize: '14px' }}
                                      value="info"
                                    >
                                      Info
                                    </MenuItem>
                                    <MenuItem
                                      sx={{ fontSize: '14px' }}
                                      value="warning"
                                    >
                                      Warning
                                    </MenuItem>
                                    <MenuItem
                                      sx={{ fontSize: '14px' }}
                                      value="error"
                                    >
                                      Error
                                    </MenuItem>
                                    <MenuItem
                                      sx={{ fontSize: '14px' }}
                                      value="critical"
                                    >
                                      Critical
                                    </MenuItem>
                                  </Select>
                                </Box>
                              ) : (
                                <>
                                  {value === 'true' || value === 'false' ? (
                                    <FormControl>
                                      <FormLabel
                                        id="demo-row-radio-buttons-group-label"
                                        sx={(theme) => ({
                                          fontSize: '14px',
                                          color: 'text.primary',
                                        })}
                                      >
                                        {' '}
                                        {getSettingsName(key)}
                                      </FormLabel>
                                      <RadioGroup
                                        row
                                        aria-labelledby="demo-row-radio-buttons-group-label"
                                        name={key}
                                        value={value}
                                        onChange={(e) => handleChange(e, key)}
                                      >
                                        <FormControlLabel
                                          value="true"
                                          disabled={isDisabled}
                                          control={<Radio />}
                                          label={
                                            <Typography
                                              sx={{ fontSize: '14px' }}
                                            >
                                              True
                                            </Typography>
                                          }
                                        />
                                        <FormControlLabel
                                          value="false"
                                          disabled={isDisabled}
                                          control={<Radio />}
                                          label={
                                            <Typography
                                              sx={{ fontSize: '14px' }}
                                            >
                                              False
                                            </Typography>
                                          }
                                        />
                                      </RadioGroup>
                                    </FormControl>
                                  ) : (
                                    <>
                                      <InputLabel
                                        variant="standard"
                                        htmlFor="uncontrolled-native"
                                        sx={{
                                          fontSize: '14px',
                                          mb: 1,
                                          color: 'text.primary',
                                        }}
                                      >
                                        {getLabelName(key)}
                                      </InputLabel>
                                      <Input
                                        sx={{
                                          px: 2,
                                          py: 0.5,
                                          width: '360px',
                                          height: '32px',
                                          border: '1px solid #303067',
                                          borderRadius: '60px',
                                          fontSize: '14px',
                                          color: (theme) =>
                                            theme.palette.text.secondary,
                                        }}
                                        disabled={isDisabled}
                                        autoComplete="off"
                                        onKeyDown={handleKeypress}
                                        name={key}
                                        onChange={(e) => onInputChange(e, key)}
                                        value={value}
                                        disableUnderline
                                        placeholder={key}
                                      />
                                    </>
                                  )}
                                </>
                              )}
                            </>
                          )}
                        </Box>
                      )
                    })}

                    {!isDisabled && (
                      <Stack
                        spacing={2}
                        direction="row"
                        sx={{ float: 'right' }}
                      >
                        <Button
                          variant="outlined"
                          onClick={() => cancelButton()}
                          sx={(theme) => ({
                            padding: '8px 20px',
                            border: '1px solid #6473FF',
                            borderRadius: '60px',
                            color: 'white',
                            fontSize: '14px',
                            textTransform: 'capitalize',
                            width: '77px',
                            height: '32px',
                          })}
                        >
                          Cancel
                        </Button>
                        <Button
                          var
                          type="submit"
                          sx={(theme) => ({
                            background: '#5552FF',
                            borderRadius: '60px',
                            color: 'white',
                            padding: '8px 30px',
                            fontSize: '14px',
                            textTransform: 'capitalize',
                            width: '63px',
                            height: '32px',
                          })}
                        >
                          Save
                        </Button>
                      </Stack>
                    )}
                  </form>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </Box>
      ) : (
        <Box sx={{ width: '100%' }}>
          <Skeleton />
          <Skeleton animation="wave" />
          <Skeleton animation={false} />
        </Box>
      )
      }
    </Container >
  )
}

export default SettingsCard
